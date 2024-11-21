from __future__ import annotations

from pydantic import BaseModel, HttpUrl


class RunWorkflowRequestFile(BaseModel):
    type: str | None = None
    transfer_method: str | None = None
    url: HttpUrl | None = None
    upload_file_id: str | None = None

    @staticmethod
    def builder() -> RunWorkflowRequestFileBuilder:
        return RunWorkflowRequestFileBuilder()


class RunWorkflowRequestFileBuilder:
    def __init__(self):
        self._run_workflow_request_file = RunWorkflowRequestFile()

    def type(self, type_: str):
        self._run_workflow_request_file.type = type_
        return self

    def transfer_method(self, transfer_method: str):
        if transfer_method not in ("remote_url", "local_file"):
            raise ValueError("Only 'remote_url' and 'local_file' are supported")
        self._run_workflow_request_file.transfer_method = transfer_method
        return self

    def url(self, url: str):
        self._run_workflow_request_file.url = HttpUrl(url=url)
        return self

    def upload_file_id(self, upload_file_id: str):
        self._run_workflow_request_file.upload_file_id = upload_file_id
        return self

    def build(self) -> RunWorkflowRequestFile:
        if (
            self._run_workflow_request_file.transfer_method == "remote_url"
            and self._run_workflow_request_file.url is None
        ):
            raise ValueError("Url needs to be set when transfer_method is set as remote_url")
        if (
            self._run_workflow_request_file.transfer_method == "local_file"
            and self._run_workflow_request_file.upload_file_id is None
        ):
            raise ValueError("Upload file_id needs to be set when transfer_method is set as local_file")
        return self._run_workflow_request_file