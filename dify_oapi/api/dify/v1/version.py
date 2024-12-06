from dify_oapi.core.model.config import Config

from .resource import Audio, File, Info, Message, Meta, Parameter


class V1:
    def __init__(self, config: Config):
        self.meta: Meta = Meta(config)
        self.file: File = File(config)
        self.audio: Audio = Audio(config)
        self.parameter: Parameter = Parameter(config)
        self.message: Message = Message(config)
        self.info: Info = Info(config)
