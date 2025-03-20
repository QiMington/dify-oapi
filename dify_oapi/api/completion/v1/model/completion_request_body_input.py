from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class CompletionRequestBodyInput(BaseModel):
    query: str | None = None
    custom_inputs: dict[str, Any] | None = Field(None, exclude=True)

    @staticmethod
    def builder() -> CompletionRequestBodyInputBuilder:
        return CompletionRequestBodyInputBuilder()


class CompletionRequestBodyInputBuilder:
    def __init__(self):
        self._completion_request_body_input = CompletionRequestBodyInput()

    def build(self) -> CompletionRequestBodyInput:
        if self._completion_request_body_input.query is None:
            raise ValueError("CompletionRequestBodyInput.query is None")
        return self._completion_request_body_input

    def query(self, query: str):
        self._completion_request_body_input.query = query
        return self

    def custom_input(self, key: str, value: Any):
        if self._completion_request_body_input.custom_inputs is None:
            self._completion_request_body_input.custom_inputs = {}
        self._completion_request_body_input.custom_inputs[key] = value
        return self

    def custom_inputs(self, custom_inputs: dict[str, Any]):
        self._completion_request_body_input.custom_inputs = custom_inputs
        return self
