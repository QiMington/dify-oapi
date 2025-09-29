import asyncio
import json
from collections.abc import AsyncGenerator, Coroutine
from typing import Literal, overload

import backoff
import httpx
from httpx import Response

from dify_oapi.core.const import SLEEP_BASE_TIME
from dify_oapi.core.json import JSON
from dify_oapi.core.log import logger
from dify_oapi.core.model.base_request import BaseRequest
from dify_oapi.core.model.base_response import BaseResponse
from dify_oapi.core.model.config import Config
from dify_oapi.core.model.request_option import RequestOption
from dify_oapi.core.type import T

from ._misc import _backoff_wait_expo, _build_header, _build_url, _unmarshaller
from .request_context.context import RequestContext
from .request_context.hooks import log_backoff, log_giveup, log_success


class ATransport:
    @staticmethod
    @overload
    def aexecute(
        conf: Config,
        req: BaseRequest,
        *,
        stream: Literal[True],
        option: RequestOption | None,
    ) -> Coroutine[None, None, AsyncGenerator[bytes, None]]: ...

    @staticmethod
    @overload
    def aexecute(conf: Config, req: BaseRequest) -> Coroutine[None, None, BaseResponse]: ...

    @staticmethod
    @overload
    def aexecute(
        conf: Config, req: BaseRequest, *, option: RequestOption | None
    ) -> Coroutine[None, None, BaseResponse]: ...

    @staticmethod
    @overload
    def aexecute(
        conf: Config,
        req: BaseRequest,
        *,
        unmarshal_as: type[T],
        option: RequestOption | None,
    ) -> Coroutine[None, None, T]: ...

    @staticmethod
    async def aexecute(
        conf: Config,
        req: BaseRequest,
        *,
        stream: bool = False,
        unmarshal_as: type[T] | type[BaseResponse] | None = None,
        option: RequestOption | None = None,
    ):
        if unmarshal_as is None:
            unmarshal_as = BaseResponse
        if option is None:
            option = RequestOption()

        # 拼接url
        url: str = _build_url(conf.domain, req.uri, req.paths)

        # 组装header
        headers: dict[str, str] = _build_header(req, option)

        json_, files, data = None, None, None
        if req.files:
            # multipart/form-data
            files = req.files
            if req.body is not None:
                data = json.loads(JSON.marshal(req.body))
        elif req.body is not None:
            # application/json
            json_ = json.loads(JSON.marshal(req.body))
        if req.http_method is None:
            raise RuntimeError("Http method is required")
        request_context = RequestContext(
            req=req,
            url=url,
            headers=headers,
            json_=json_,
            data=data,
            files=files,
            http_method=req.http_method,
        )
        if stream:
            return _async_stream_generator(conf, request_context)
        response = await _async_block_generator(conf, request_context)

        return _unmarshaller(unmarshal_as, http_resp=response)


async def _async_stream_generator(conf: Config, ctx: RequestContext, /) -> AsyncGenerator[bytes, None]:
    details = {"tries": 1, "wait": 0.0, "exception": None}
    for attempt in range(1, conf.max_retry_count + 2):
        try:
            async with httpx.AsyncClient() as ac, ac.stream(
                ctx.http_method.name,
                ctx.url,
                headers=ctx.headers,
                params=tuple(ctx.req.queries),
                json=ctx.json_,
                data=ctx.data,
                files=ctx.files,
                timeout=conf.timeout,
            ) as async_response:
                if async_response.status_code != 200:
                    try:
                        error_detail = await async_response.read()
                        error_message = error_detail.decode("utf-8", errors="ignore")
                    except Exception:
                        error_message = f"Error response with status code {async_response.status_code}"
                    error_message = error_message.strip()
                    logger.warning(f"Streaming request failed: {async_response.status_code}, detail: {error_message}")
                    yield f"data: [ERROR] {error_message}\n\n".encode()
                else:
                    try:
                        async for chunk in async_response.aiter_bytes():
                            yield chunk
                    except Exception as chunk_e:
                        logger.exception("Streaming failed during chunk reading")
                        yield f"data: [ERROR] Stream interrupted: {str(chunk_e)}\n\n".encode()
                log_success(ctx)(details)
                return
        except httpx.RequestError as e:
            wait_time = _backoff_wait_expo(attempt)
            details = {"tries": attempt, "wait": wait_time, "exception": e}
            if attempt - 1 < conf.max_retry_count:
                log_backoff(ctx)(details)
                await asyncio.sleep(wait_time)
            else:
                log_giveup(ctx)(details)
                raise e


async def _async_block_generator(conf: Config, ctx: RequestContext, /) -> Response:
    @backoff.on_exception(
        backoff.expo,
        (httpx.RequestError,),
        max_tries=conf.max_retry_count + 1,
        on_backoff=log_backoff(ctx),
        on_giveup=log_giveup(ctx),
        on_success=log_success(ctx),
        logger=None,
        jitter=None,
        factor=SLEEP_BASE_TIME,
    )
    async def inner_run():
        async with httpx.AsyncClient() as client:
            response = await client.request(
                ctx.http_method.name,
                ctx.url,
                headers=ctx.headers,
                params=tuple(ctx.req.queries),
                json=ctx.json_,
                data=ctx.data,
                files=ctx.files,
                timeout=conf.timeout,
            )
            return response

    return await inner_run()
