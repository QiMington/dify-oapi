from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

from .document_request_process_rule import DocumentRequestProcessRule


class CreateDocumentByFileRequestBodyData(BaseModel):
    original_document_id: str | None = None
    indexing_technique: str | None = None
    process_rule: DocumentRequestProcessRule | None = None

    @staticmethod
    def builder() -> CreateDocumentByFileRequestBodyDataBuilder:
        return CreateDocumentByFileRequestBodyDataBuilder()


class CreateDocumentByFileRequestBodyDataBuilder:
    def __init__(self):
        create_document_by_file_request_body_data = CreateDocumentByFileRequestBodyData()
        self._create_document_by_file_request_body_data = create_document_by_file_request_body_data

    def build(self) -> CreateDocumentByFileRequestBodyData:
        return self._create_document_by_file_request_body_data

    def original_document_id(self, original_document_id: str) -> CreateDocumentByFileRequestBodyDataBuilder:
        self._create_document_by_file_request_body_data.original_document_id = original_document_id
        return self

    def indexing_technique(
        self, indexing_technique: Literal["high_quality", "economy"]
    ) -> CreateDocumentByFileRequestBodyDataBuilder:
        self._create_document_by_file_request_body_data.indexing_technique = indexing_technique
        return self

    def process_rule(self, process_rule: DocumentRequestProcessRule) -> CreateDocumentByFileRequestBodyDataBuilder:
        self._create_document_by_file_request_body_data.process_rule = process_rule
        return self
