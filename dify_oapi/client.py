from __future__ import annotations

from .api.chat.service import ChatService
from .api.completion.service import CompletionService
from .api.dify.service import DifyService
from .api.knowledge_base.service import KnowledgeBaseService
from .api.workflow.service import WorkflowService
from .core.enum import LogLevel
from .core.http.transport import Transport
from .core.log import logger
from .core.model.base_request import BaseRequest
from .core.model.config import Config


class Client:
    def __init__(self):
        self._config: Config | None = None
        self._chat: ChatService | None = None
        self._completion: CompletionService | None = None
        self._dify: DifyService | None = None
        self._workflow: WorkflowService | None = None
        self._knowledge_base: KnowledgeBaseService | None = None

    @property
    def chat(self) -> ChatService:
        if self._chat is None:
            raise RuntimeError("Chat service has not been initialized")
        return self._chat

    @property
    def completion(self) -> CompletionService:
        if self._completion is None:
            raise RuntimeError("Completion service has not been initialized")
        return self._completion

    @property
    def dify(self) -> DifyService:
        if self._dify is None:
            raise RuntimeError("Dify service has not been initialized")
        return self._dify

    @property
    def workflow(self) -> WorkflowService:
        if self._workflow is None:
            raise RuntimeError("Workflow service has not been initialized")
        return self._workflow

    @property
    def knowledge_base(self) -> KnowledgeBaseService:
        if self._knowledge_base is None:
            raise RuntimeError("Knowledge base service has not been initialized")
        return self._knowledge_base

    def request(self, request: BaseRequest):
        if self._config is None:
            raise RuntimeError("Config is not set")
        resp = Transport.execute(self._config, request)
        return resp

    @staticmethod
    def builder() -> ClientBuilder:
        return ClientBuilder()


class ClientBuilder:
    def __init__(self) -> None:
        self._config = Config()

    def domain(self, domain: str) -> ClientBuilder:
        self._config.domain = domain
        return self

    def log_level(self, level: LogLevel) -> ClientBuilder:
        self._config.log_level = level
        return self

    def max_retry_count(self, count: int) -> ClientBuilder:
        self._config.max_retry_count = count
        return self

    def build(self) -> Client:
        client: Client = Client()
        client._config = self._config

        # 初始化日志
        self._init_logger()

        # 初始化 服务
        client._chat = ChatService(self._config)
        client._completion = CompletionService(self._config)
        client._dify = DifyService(self._config)
        client._workflow = WorkflowService(self._config)
        client._knowledge_base = KnowledgeBaseService(self._config)
        return client

    def _init_logger(self):
        logger.setLevel(int(self._config.log_level.value))
