from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

from .document_request_process_rule import DocumentRequestProcessRule


class UpdateDocumentByFileRequestBodyData(BaseModel):
    name: str | None = None
    indexing_technique: str | None = None
    process_rule: DocumentRequestProcessRule | None = None

    @staticmethod
    def builder() -> UpdateDocumentByFileRequestBodyDataBuilder:
        return UpdateDocumentByFileRequestBodyDataBuilder()


class UpdateDocumentByFileRequestBodyDataBuilder:
    def __init__(self):
        update_document_by_file_request_body_data = UpdateDocumentByFileRequestBodyData()
        self._update_document_by_file_request_body_data = update_document_by_file_request_body_data

    def build(self) -> UpdateDocumentByFileRequestBodyData:
        return self._update_document_by_file_request_body_data

    def name(self, name: str) -> UpdateDocumentByFileRequestBodyDataBuilder:
        self._update_document_by_file_request_body_data.name = name
        return self

    def indexing_technique(
        self, indexing_technique: Literal["high_quality", "economy"]
    ) -> UpdateDocumentByFileRequestBodyDataBuilder:
        self._update_document_by_file_request_body_data.indexing_technique = indexing_technique
        return self

    def process_rule(self, process_rule: DocumentRequestProcessRule) -> UpdateDocumentByFileRequestBodyDataBuilder:
        self._update_document_by_file_request_body_data.process_rule = process_rule
        return self
