import json
import time
from collections.abc import Generator
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


def _stream_generator(
    conf: Config,
    req: BaseRequest,
    *,
    url: str,
    headers: dict[str, str],
    json_: dict | None,
    data: dict | None,
    files: dict | None,
    http_method: HttpMethod,
) -> Generator[bytes, None, None]:
    http_method_name = str(http_method.name)
    stream_retry_count = conf.max_retry_count
    for stream_retry in range(0, stream_retry_count + 1):
        # 采用指数避让策略
        if stream_retry != 0:
            stream_sleep_time = _get_sleep_time(stream_retry)
            logger.info(f"in-request: sleep {stream_sleep_time}s")
            time.sleep(stream_sleep_time)
        try:
            with (
                httpx.Client() as _client,
                _client.stream(
                    http_method_name,
                    url,
                    headers=headers,
                    params=tuple(req.queries),
                    json=json_,
                    data=data,
                    files=files,
                    timeout=conf.timeout,
                ) as sync_response,
            ):
                logger.debug(
                    f"{http_method_name} {url} {sync_response.status_code}, "
                    f"headers: {JSON.marshal(headers)}, "
                    f"params: {JSON.marshal(req.queries)}, "
                    f"stream response"
                )
                if sync_response.status_code != 200:
                    try:
                        error_detail = sync_response.read()
                        error_message = error_detail.decode("utf-8", errors="ignore")
                    except Exception:
                        error_message = f"Error response with status code {sync_response.status_code}"
                    error_message = error_message.strip()
                    logger.warning(f"Streaming request failed: {sync_response.status_code}, detail: {error_message}")
                    yield f"data: [ERROR] {error_message}\n\n".encode()
                    return
                try:
                    yield from sync_response.iter_bytes()
                except Exception as chunk_e:
                    logger.exception("Streaming failed during chunk reading")
                    yield f"data: [ERROR] Stream interrupted: {str(chunk_e)}\n\n".encode()
                return
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
        http_method_name = str(req.http_method.name)
        if stream:
            return _stream_generator(
                conf=conf,
                req=req,
                url=url,
                headers=headers,
                json_=json_,
                data=data,
                files=files,
                http_method=req.http_method,
            )
        with httpx.Client() as client:
            # 通过变量赋值，防止动态调整 max_retry_count 出现并发问题
            retry_count = conf.max_retry_count
            for i in range(0, retry_count + 1):
                # 采用指数避让策略
                if i != 0:
                    sleep_time = _get_sleep_time(i)
                    logger.info(f"in-request: sleep {sleep_time}s")
                    time.sleep(sleep_time)
                try:
                    response = client.request(
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
