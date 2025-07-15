from __future__ import annotations

from pydantic import BaseModel

from .update_document_by_text_request_body_data import UpdateDocumentByTextRequestBodyData


class UpdateDocumentByTextRequestBody(BaseModel):
    data: str | None = None

    @staticmethod
    def builder() -> UpdateDocumentByTextRequestBodyBuilder:
        return UpdateDocumentByTextRequestBodyBuilder()


class UpdateDocumentByTextRequestBodyBuilder:
    def __init__(self):
        update_document_by_text_request_body = UpdateDocumentByTextRequestBody()
        self._update_document_by_text_request_body = update_document_by_text_request_body

    def build(self) -> UpdateDocumentByTextRequestBody:
        return self._update_document_by_text_request_body

    def data(self, data: UpdateDocumentByTextRequestBodyData) -> UpdateDocumentByTextRequestBodyBuilder:
        self._update_document_by_text_request_body.data = data.model_dump_json(exclude_none=True)
        return self
