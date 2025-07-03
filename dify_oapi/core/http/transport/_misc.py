import math

from dify_oapi.core.const import APPLICATION_JSON, AUTHORIZATION, SLEEP_BASE_TIME, UTF_8
from dify_oapi.core.json import JSON
from dify_oapi.core.log import logger
from dify_oapi.core.misc import HiddenText
from dify_oapi.core.model.base_request import BaseRequest
from dify_oapi.core.model.raw_response import RawResponse
from dify_oapi.core.model.request_option import RequestOption
from dify_oapi.core.type import T


def _build_url(domain: str | None, uri: str | None, paths: dict[str, str] | None) -> str:
    if domain is None:
        raise RuntimeError("domain is required")
    if uri is None:
        raise RuntimeError("uri is required")
    for key, value in (paths or {}).items():
        uri = uri.replace(":" + key, value)
    if domain.endswith("/") and uri.startswith("/"):
        domain = domain[:-1]
    return domain + uri


def _build_header(request: BaseRequest, option: RequestOption) -> dict[str, str]:
    headers = request.headers
    # 附加header
    if option.headers is not None:
        for key in option.headers:
            headers[key] = option.headers[key]
    if option.api_key is not None:
        headers[AUTHORIZATION] = HiddenText(f"Bearer {option.api_key}", redacted="****")
    return headers


def _merge_dicts(*dicts):
    res = {}
    for d in dicts:
        if d is not None:
            res.update(d)
    return res


def _unmarshaller(raw_resp: RawResponse, unmarshal_as: type[T]) -> T:
    if raw_resp.status_code is None:
        raise RuntimeError("status_code is required")
    if raw_resp.content is None:
        raise RuntimeError("status_code is required")
    resp = unmarshal_as()
    if raw_resp.content_type is not None and raw_resp.content_type.startswith(APPLICATION_JSON):
        content = str(raw_resp.content, UTF_8)
        if content != "":
            try:
                resp = JSON.unmarshal(content, unmarshal_as)
            except Exception as e:
                logger.error(f"Failed to unmarshal to {unmarshal_as} from {content}")
                raise e
    resp.raw = raw_resp
    # if 200 <= raw_resp.status_code < 300:
    #     resp.code = "success"
    return resp


def _get_sleep_time(retry_count: int):
    sleep_time = SLEEP_BASE_TIME * math.pow(2, retry_count - 1)
    # if sleep_time > 60:
    #     sleep_time = 60
    # if raw_resp and (raw_resp.status_code == 429 or raw_resp.status_code == 503) and 'retry-after' in raw_resp.headers:
    #     try:
    #         sleep_time = max(int(raw_resp.headers['retry-after']), sleep_time)
    #     except Exception as e:
    #         logger.warning('try to parse retry-after from headers error: {}'.format(e))
    return sleep_time
