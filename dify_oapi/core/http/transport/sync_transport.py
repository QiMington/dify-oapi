import json
import time
from collections.abc import Generator
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
from dify_oapi.core.model.raw_response import RawResponse
from dify_oapi.core.model.request_option import RequestOption
from dify_oapi.core.type import T

from ._misc import _backoff_wait_expo, _build_header, _build_url, _unmarshaller
from .request_context.context import RequestContext
from .request_context.hooks import log_backoff, log_giveup, log_success


class Transport:
    @staticmethod
    @overload
    def execute(
        conf: Config,
        req: BaseRequest,
        *,
        stream: Literal[True],
        option: RequestOption | None,
    ) -> Generator[bytes, None, None]: ...

    @staticmethod
    @overload
    def execute(conf: Config, req: BaseRequest) -> BaseResponse: ...

    @staticmethod
    @overload
    def execute(conf: Config, req: BaseRequest, *, option: RequestOption | None) -> BaseResponse: ...

    @staticmethod
    @overload
    def execute(
        conf: Config,
        req: BaseRequest,
        *,
        unmarshal_as: type[T],
        option: RequestOption | None,
    ) -> T: ...

    @staticmethod
    def execute(
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
            raise RuntimeError("HTTP method is required")
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
            return _stream_generator(conf, request_context)
        response = _block_generator(conf, request_context)
        raw_resp = RawResponse()
        raw_resp.status_code = response.status_code
        raw_resp.headers = dict(response.headers)
        raw_resp.content = response.content
        return _unmarshaller(raw_resp, unmarshal_as)


def _stream_generator(conf: Config, ctx: RequestContext, /) -> Generator[bytes, None, None]:
    details = {"tries": 1, "wait": 0.0, "exception": None}
    for attempt in range(1, conf.max_retry_count + 2):
        try:
            with httpx.stream(
                ctx.http_method.name,
                ctx.url,
                headers=ctx.headers,
                params=tuple(ctx.req.queries),
                json=ctx.json_,
                data=ctx.data,
                files=ctx.files,
                timeout=conf.timeout,
            ) as sync_response:
                if sync_response.status_code != 200:
                    try:
                        error_detail = sync_response.read()
                        error_message = error_detail.decode("utf-8", errors="ignore")
                    except Exception:
                        error_message = f"Error response with status code {sync_response.status_code}"
                    error_message = error_message.strip()
                    logger.warning(f"Streaming request failed: {sync_response.status_code}, detail: {error_message}")
                    yield f"data: [ERROR] {error_message}\n\n".encode()
                else:
                    try:
                        yield from sync_response.iter_bytes()
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
                time.sleep(wait_time)
            else:
                log_giveup(ctx)(details)
                raise e


def _block_generator(conf: Config, ctx: RequestContext, /) -> Response:
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
    def inner_run():
        with httpx.Client() as client:
            response = client.request(
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

    return inner_run()
