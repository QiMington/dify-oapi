import asyncio
import json
from collections.abc import AsyncGenerator, Coroutine
from typing import Literal, overload

import httpx

from dify_oapi.core.enum import HttpMethod
from dify_oapi.core.json import JSON
from dify_oapi.core.log import logger
from dify_oapi.core.model.base_request import BaseRequest
from dify_oapi.core.model.base_response import BaseResponse
from dify_oapi.core.model.config import Config
from dify_oapi.core.model.raw_response import RawResponse
from dify_oapi.core.model.request_option import RequestOption
from dify_oapi.core.type import T

from ._misc import _build_header, _build_url, _get_sleep_time, _merge_dicts, _unmarshaller


async def _async_stream_generator(
    conf: Config,
    req: BaseRequest,
    *,
    url: str,
    headers: dict[str, str],
    json_: dict | None,
    data: dict | None,
    files: dict | None,
    http_method: HttpMethod,
):
    http_method_name = str(http_method.name)
    stream_retry_count = conf.max_retry_count
    for stream_retry in range(0, stream_retry_count + 1):
        # 采用指数避让策略
        if stream_retry != 0:
            stream_sleep_time = _get_sleep_time(stream_retry)
            logger.info(f"in-request: sleep {stream_sleep_time}s")
            await asyncio.sleep(stream_sleep_time)
        try:
            async with (
                httpx.AsyncClient() as _client,
                _client.stream(
                    http_method_name,
                    url,
                    headers=headers,
                    params=tuple(req.queries),
                    json=json_,
                    data=data,
                    files=files,
                    timeout=conf.timeout,
                ) as async_response,
            ):
                logger.debug(
                    f"{http_method_name} {url} {async_response.status_code}, "
                    f"headers: {JSON.marshal(headers)}, "
                    f"params: {JSON.marshal(req.queries)}, "
                    f"stream response"
                )
                if async_response.status_code != 200:
                    try:
                        error_detail = await async_response.aread()
                        error_message = error_detail.decode("utf-8", errors="ignore")
                    except Exception:
                        error_message = f"Error response with status code {async_response.status_code}"
                    error_message = error_message.strip()
                    logger.warning(f"Streaming request failed: {async_response.status_code}, detail: {error_message}")
                    yield f"data: [ERROR] {error_message}\n\n".encode()
                    return
                try:
                    async for chunk in async_response.aiter_bytes():
                        yield chunk
                except Exception as chunk_e:
                    logger.exception("Streaming failed during chunk reading")
                    yield f"data: [ERROR] Stream interrupted: {str(chunk_e)}\n\n".encode()
                break
        except httpx.RequestError as r_e:
            if stream_retry < stream_retry_count:
                logger.info(
                    f"in-request: retry success "
                    f"{http_method_name} {url}"
                    f"{f', headers: {JSON.marshal(headers)}' if headers else ''}"
                    f"{f', params: {JSON.marshal(req.queries)}' if req.queries else ''}"
                    f"{f', body: {JSON.marshal(_merge_dicts(json_, files, data))}' if json_ or files or data else ''}"
                    f"{f', exp: {r_e}'}"
                )
                continue
            logger.info(
                f"in-request: retry fail "
                f"{http_method_name} {url}"
                f"{f', headers: {JSON.marshal(headers)}' if headers else ''}"
                f"{f', params: {JSON.marshal(req.queries)}' if req.queries else ''}"
                f"{f', body: {JSON.marshal(_merge_dicts(json_, files, data))}' if json_ or files or data else ''}"
                f"{f', exp: {r_e}'}"
            )
            raise r_e


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
        http_method_name = str(req.http_method.name)
        if stream:
            return _async_stream_generator(
                conf=conf,
                req=req,
                url=url,
                headers=headers,
                json_=json_,
                data=data,
                files=files,
                http_method=req.http_method,
            )
        async with httpx.AsyncClient() as client:
            # 通过变量赋值，防止动态调整 max_retry_count 出现并发问题
            retry_count = conf.max_retry_count
            for i in range(0, retry_count + 1):
                # 采用指数避让策略
                if i != 0:
                    sleep_time = _get_sleep_time(i)
                    logger.info(f"in-request: sleep {sleep_time}s")
                    await asyncio.sleep(sleep_time)
                try:
                    response = await client.request(
                        http_method_name,
                        url,
                        headers=headers,
                        params=tuple(req.queries),
                        json=json_,
                        data=data,
                        files=files,
                        timeout=conf.timeout,
                    )
                    break
                except httpx.RequestError as e:
                    if i < retry_count:
                        logger.info(
                            f"in-request: retry success "
                            f"{http_method_name} {url}"
                            f"{f', headers: {JSON.marshal(headers)}' if headers else ''}"
                            f"{f', params: {JSON.marshal(req.queries)}' if req.queries else ''}"
                            f"{f', body: {JSON.marshal(_merge_dicts(json_, files, data))}' if json_ or files or data else ''}"
                            f"{f', exp: {e}'}"
                        )
                        continue
                    logger.info(
                        f"in-request: retry fail "
                        f"{http_method_name} {url}"
                        f"{f', headers: {JSON.marshal(headers)}' if headers else ''}"
                        f"{f', params: {JSON.marshal(req.queries)}' if req.queries else ''}"
                        f"{f', body: {JSON.marshal(_merge_dicts(json_, files, data))}' if json_ or files or data else ''}"
                        f"{f', exp: {e}'}"
                    )
                    raise e

            logger.debug(
                f"{http_method_name} {url} {response.status_code}"
                f"{f', headers: {JSON.marshal(headers)}' if headers else ''}"
                f"{f', params: {JSON.marshal(req.queries)}' if req.queries else ''}"
                f"{f', body: {JSON.marshal(_merge_dicts(json_, files, data))}' if json_ or files or data else ''}"
            )

            raw_resp = RawResponse()
            raw_resp.status_code = response.status_code
            raw_resp.headers = dict(response.headers)
            raw_resp.content = response.content

            return _unmarshaller(raw_resp, unmarshal_as)
