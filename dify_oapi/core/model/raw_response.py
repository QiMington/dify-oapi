import json

from pydantic import BaseModel, Field

from dify_oapi.core.const import CONTENT_TYPE


class RawResponse(BaseModel):
    status_code: int | None = None
    headers: dict[str, str] = Field(default_factory=dict)
    content: bytes | None = None

    def set_content_type(self, content_type: str) -> None:
        self.headers[CONTENT_TYPE.lower()] = content_type

    def set_error_content(self, message: str | bytes):
        if isinstance(message, bytes):
            message_string = message.decode("utf-8", errors="ignore")
        else:
            message_string = message
        self.content = json.dumps({"message": message_string}).encode("utf-8")

    @property
    def content_type(self) -> str | None:
        content_type = self.headers.get(CONTENT_TYPE) or self.headers.get(CONTENT_TYPE.lower())
        return content_type
