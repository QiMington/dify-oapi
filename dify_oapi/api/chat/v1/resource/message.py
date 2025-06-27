from dify_oapi.core.http.transport import ATransport, Transport
from dify_oapi.core.model.config import Config
from dify_oapi.core.model.request_option import RequestOption

from ..model.message_history_request import MessageHistoryRequest
from ..model.message_history_response import MessageHistoryResponse
from ..model.message_suggested_request import MessageSuggestedRequest
from ..model.message_suggested_response import MessageSuggestedResponse


class Message:
    def __init__(self, config: Config) -> None:
        self.config: Config = config

    def suggested(
        self, request: MessageSuggestedRequest, option: RequestOption | None = None
    ) -> MessageSuggestedResponse:
        # 发起请求
        return Transport.execute(self.config, request, unmarshal_as=MessageSuggestedResponse, option=option)

    async def asuggested(
        self, request: MessageSuggestedRequest, option: RequestOption | None = None
    ) -> MessageSuggestedResponse:
        # 发起请求
        return await ATransport.aexecute(self.config, request, unmarshal_as=MessageSuggestedResponse, option=option)

    def history(self, request: MessageHistoryRequest, option: RequestOption | None = None) -> MessageHistoryResponse:
        # 发起请求
        return Transport.execute(self.config, request, unmarshal_as=MessageHistoryResponse, option=option)

    async def ahistory(
        self, request: MessageHistoryRequest, option: RequestOption | None = None
    ) -> MessageHistoryResponse:
        # 发起请求
        return await ATransport.aexecute(self.config, request, unmarshal_as=MessageHistoryResponse, option=option)
