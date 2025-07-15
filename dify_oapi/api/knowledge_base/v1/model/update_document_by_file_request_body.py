from __future__ import annotations

from pydantic import BaseModel

from .update_document_by_file_request_body_data import UpdateDocumentByFileRequestBodyData


class UpdateDocumentByFileRequestBody(BaseModel):
    data: str | None = None

    @staticmethod
    def builder() -> UpdateDocumentByFileRequestBodyBuilder:
        return UpdateDocumentByFileRequestBodyBuilder()


class UpdateDocumentByFileRequestBodyBuilder:
    def __init__(self):
        update_document_by_file_request_body = UpdateDocumentByFileRequestBody()
        self._update_document_by_file_request_body = update_document_by_file_request_body

    def build(self) -> UpdateDocumentByFileRequestBody:
        return self._update_document_by_file_request_body

    def data(self, data: UpdateDocumentByFileRequestBodyData) -> UpdateDocumentByFileRequestBodyBuilder:
        self._update_document_by_file_request_body.data = data.model_dump_json(exclude_none=True)
        return self
