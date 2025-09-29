import json
from collections.abc import AsyncGenerator, Generator
from typing import Literal, overload

from core.const import APPLICATION_JSON
from core.http.transport._misc import _unmarshaller
from core.model.raw_response import RawResponse

from dify_oapi.core.http.transport import ATransport, Transport
from dify_oapi.core.model.config import Config
from dify_oapi.core.model.request_option import RequestOption

from ..model.get_workflow_log_request import GetWorkflowLogRequest
from ..model.get_workflow_log_response import GetWorkflowLogResponse
from ..model.get_workflow_result_request import GetWorkflowResultRequest
from ..model.get_workflow_result_response import GetWorkflowResultResponse
from ..model.run_workflow_request import RunWorkflowRequest
from ..model.run_workflow_response import RunWorkflowResponse
from ..model.stop_workflow_request import StopWorkflowRequest
from ..model.stop_workflow_response import StopWorkflowResponse


class Workflow:
    def __init__(self, config: Config) -> None:
        self.config: Config = config

    @overload
    def run(
        self,
        request: RunWorkflowRequest,
        option: RequestOption | None,
        stream: Literal[True],
    ) -> Generator[bytes, None, None]: ...

    @overload
    def run(
        self,
        request: RunWorkflowRequest,
        option: RequestOption | None,
        stream: Literal[False],
        *,
        block_via_stream: bool = False,
    ) -> RunWorkflowResponse: ...

    @overload
    def run(
        self,
        request: RunWorkflowRequest,
        option: RequestOption | None,
        *,
        block_via_stream: bool = False,
    ) -> RunWorkflowResponse: ...

    def run(
        self,
        request: RunWorkflowRequest,
        option: RequestOption | None = None,
        stream: bool = False,
        *,
        block_via_stream: bool = False,
    ):
        if stream:
            request.body["response_mode"] = "streaming"
            return Transport.execute(self.config, request, option=option, stream=True)
        if not block_via_stream:
            request.body["response_mode"] = "blocking"
            return Transport.execute(self.config, request, unmarshal_as=RunWorkflowResponse, option=option)
        request.body["response_mode"] = "streaming"
        stream_ctx = Transport.execute(self.config, request, option=option, stream=True, return_raw_response=True)
        with stream_ctx as response:
            raw_response = RawResponse(
                status_code=response.status_code,
                headers=dict(response.headers),
            )
            if raw_response.status_code != 200:
                raw_response.content = json.dumps(
                    {
                        "message": next(response.iter_bytes(4096), b"HTTP error").decode("utf-8", errors="ignore"),
                    }
                ).encode("utf-8")
                return _unmarshaller(RunWorkflowResponse, raw_resp=raw_response)
            for line in response.iter_lines():
                if not line.startswith("data: "):
                    continue
                raw_data = line[6:]
                try:
                    data = dict(json.loads(raw_data))
                except Exception as e:
                    raw_response.status_code = 500
                    raw_response.content = json.dumps({"message": f"Invalid JSON: {e or e!r}: {raw_data}"}).encode(
                        "utf-8"
                    )
                    break
                if data.get("event") == "workflow_finished":
                    d = dict(data.get("data", {}))
                    status = d.get("status", "<UNK>")
                    if status == "succeeded":
                        raw_response.content = raw_data.encode("utf-8")
                        raw_response.set_content_type(APPLICATION_JSON)
                    else:
                        raw_response.status_code = 500
                        raw_response.content = json.dumps(
                            {"message": data.get("error", f"Invalid status: {data}")}
                        ).encode("utf-8")
                    break
            else:
                # 流结束也没拿到 workflow_finished
                raw_response.status_code = 520
                raw_response.content = json.dumps({"message": "Workflow did not finish properly"}).encode("utf-8")
            return _unmarshaller(RunWorkflowResponse, raw_resp=raw_response)

    @overload
    async def arun(
        self,
        request: RunWorkflowRequest,
        option: RequestOption | None,
        stream: Literal[True],
    ) -> AsyncGenerator[bytes, None]: ...

    @overload
    async def arun(
        self,
        request: RunWorkflowRequest,
        option: RequestOption | None,
        stream: Literal[False],
    ) -> RunWorkflowResponse: ...

    @overload
    async def arun(self, request: RunWorkflowRequest, option: RequestOption | None) -> RunWorkflowResponse: ...

    async def arun(
        self,
        request: RunWorkflowRequest,
        option: RequestOption | None = None,
        stream: bool = False,
    ):
        if stream:
            return await ATransport.aexecute(self.config, request, option=option, stream=True)
        else:
            return await ATransport.aexecute(self.config, request, unmarshal_as=RunWorkflowResponse, option=option)

    def stop(self, request: StopWorkflowRequest, option: RequestOption | None = None) -> StopWorkflowResponse:
        return Transport.execute(self.config, request, unmarshal_as=StopWorkflowResponse, option=option)

    async def astop(self, request: StopWorkflowRequest, option: RequestOption | None = None) -> StopWorkflowResponse:
        return await ATransport.aexecute(self.config, request, unmarshal_as=StopWorkflowResponse, option=option)

    def result(
        self, request: GetWorkflowResultRequest, option: RequestOption | None = None
    ) -> GetWorkflowResultResponse:
        return Transport.execute(self.config, request, unmarshal_as=GetWorkflowResultResponse, option=option)

    async def aresult(
        self, request: GetWorkflowResultRequest, option: RequestOption | None = None
    ) -> GetWorkflowResultResponse:
        return await ATransport.aexecute(self.config, request, unmarshal_as=GetWorkflowResultResponse, option=option)

    def log(self, request: GetWorkflowLogRequest, option: RequestOption | None = None) -> GetWorkflowLogResponse:
        return Transport.execute(self.config, request, unmarshal_as=GetWorkflowLogResponse, option=option)

    async def alog(self, request: GetWorkflowLogRequest, option: RequestOption | None = None) -> GetWorkflowLogResponse:
        return await ATransport.aexecute(self.config, request, unmarshal_as=GetWorkflowLogResponse, option=option)
