from pydantic import BaseModel, Field

from .raw_response import RawResponse


class BaseResponse(BaseModel):
    raw: RawResponse | None = None
    code: str | None = Field(default=None, exclude=True)
    msg_: str | None = Field(default=None, validation_alias="msg", exclude=True)
    message_: str | None = Field(default=None, validation_alias="message", exclude=True)

    @property
    def msg(self) -> str | None:
        return self.msg_ or self.message_

    @property
    def success(self) -> bool:
        return self.code is None
