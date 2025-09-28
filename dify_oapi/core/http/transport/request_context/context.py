from dataclasses import dataclass
from typing import Any

from dify_oapi.core.enum import HttpMethod
from dify_oapi.core.json import JSON
from dify_oapi.core.model.base_request import BaseRequest

from .._misc import _merge_dicts


@dataclass
class RequestContext:
    req: BaseRequest
    url: str
    headers: dict[str, str]
    json_: dict[str, Any] | None
    data: dict[str, Any] | None
    files: dict[str, Any] | None
    http_method: HttpMethod

    @property
    def log_str(self) -> str:
        return (
            f"{self.http_method.name} {self.url}"
            f"{f', headers: {JSON.marshal(self.headers)}' if self.headers else ''}"
            f"{f', params: {JSON.marshal(self.req.queries)}' if self.req.queries else ''}"
            f"{f', body: {JSON.marshal(_merge_dicts(self.json_, self.files, self.data))}' if self.json_ or self.files or self.data else ''}"
        )
