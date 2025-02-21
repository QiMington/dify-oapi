from dify_oapi.core.model.config import Config

from .resource import Audio, Chat, Conversation, Message


class V1:
    def __init__(self, config: Config):
        self.chat: Chat = Chat(config)
        self.conversation: Conversation = Conversation(config)
        self.message: Message = Message(config)
        self.audio: Audio = Audio(config)
