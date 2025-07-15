from __future__ import annotations

from pydantic import BaseModel

from .document_request_process_rule import DocumentRequestProcessRule


class UpdateDocumentByTextRequestBodyData(BaseModel):
    name: str | None = None
    text: str | None = None
    process_rule: DocumentRequestProcessRule | None = None

    @staticmethod
    def builder() -> UpdateDocumentByTextRequestBodyDataBuilder:
        return UpdateDocumentByTextRequestBodyDataBuilder()


class UpdateDocumentByTextRequestBodyDataBuilder:
    def __init__(self):
        self._update_document_by_text_request_body_data = UpdateDocumentByTextRequestBodyData()

    def build(self) -> UpdateDocumentByTextRequestBodyData:
        return self._update_document_by_text_request_body_data

    def name(self, name: str) -> UpdateDocumentByTextRequestBodyDataBuilder:
        self._update_document_by_text_request_body_data.name = name
        return self

    def text(self, text: str) -> UpdateDocumentByTextRequestBodyDataBuilder:
        self._update_document_by_text_request_body_data.text = text
        return self

    def process_rule(self, process_rule: DocumentRequestProcessRule) -> UpdateDocumentByTextRequestBodyDataBuilder:
        self._update_document_by_text_request_body_data.process_rule = process_rule
        return self
