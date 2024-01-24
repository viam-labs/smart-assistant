import asyncio

from collections.abc import Mapping, Sequence
from typing import ClassVar, cast, Optional
from typing_extensions import Self
from viam.components.generic import Generic
from viam.module.module import Model, Reconfigurable, ResourceBase, ResourceName
from viam.resource.types import ModelFamily
from viam.proto.app.robot import ComponentConfig
from viam.services.service_base import ValueTypes
from viam.utils import struct_to_dict
from viam.logging import getLogger

from chat_service_api import Chat
from speech_service_api import SpeechService

LOGGER = getLogger(__name__)

class Assistant(Generic, Reconfigurable):
    MODEL: ClassVar[Model] = Model(ModelFamily("viam-labs", "generic"), "assistant")

    chat: Chat
    speech: SpeechService
    started: asyncio.Task | None = None

    def __init__(self, name: str):
        super().__init__(name)

    @classmethod
    def new(cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        assistant = cls(config.name)
        LOGGER.info(f"Log config: {config.log_configuration}")
        LOGGER.info(f"Depends on: {config.depends_on}")
        LOGGER.info(f"Service configs: {config.service_configs}")
        assistant.reconfigure(config, dependencies)
        return assistant

    @classmethod
    def validate_config(cls, config: ComponentConfig) -> Sequence[str]:
        attrs = struct_to_dict(config.attributes)
        chat_name = attrs.get("chat_service", "")
        assert isinstance(chat_name, str)
        if (chat_name == ""):
            raise Exception("The chat_service name is required for the Assistant component")

        speech_name = attrs.get("speech_service", "")
        assert isinstance(speech_name, str)
        if (speech_name == ""):
            raise Exception("The speech_service name is required for the Assistant component")

        return [chat_name, speech_name]

    def reconfigure(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]):
        attrs = struct_to_dict(config.attributes)
        chat_name = attrs.get("chat_service")
        speech_name = attrs.get("speech_service")

        assert isinstance(chat_name, str) and isinstance(speech_name, str)

        chat = dependencies[Chat.get_resource_name(chat_name)]
        speech = dependencies[SpeechService.get_resource_name(speech_name)]

        self.chat = cast(Chat, chat)
        self.speech = cast(SpeechService, speech)

        LOGGER.info(f"Found chat service {chat_name}: {self.chat}")
        LOGGER.info(f"Found speech service {speech_name}: {self.speech}")

        if hasattr(self, "started") and self.started is not None:
            self.started.cancel()

        self.started = asyncio.create_task(self.start())

    async def do_command(self, command: Mapping[str, ValueTypes], *, timeout: Optional[float] = None, **kwargs) -> Mapping[str, ValueTypes]:
        for command_name, args in command.items():
            if command_name == "intro":
                return {
                        "intro": await self.intro()
                        }
            if command_name == "restart":
                return {
                        "restart": await self.restart()
                        }
            else:
                LOGGER.warning(f"Unknown command: {command_name}")
                return {}
        return {}

    async def close(self):
        if self.started is not None:
            self.started.cancel()
            await self.started

    async def start(self):
        LOGGER.info("Started assistant!")

        await self.speech.say("Hello from your Viam smart assistant! How can I help you today?", blocking=True)

    async def restart(self):
        if self.started is not None:
            self.started.cancel()
            await self.started

        self.started = asyncio.create_task(self.start())

        return "Restart complete"

    async def intro(self):
        LOGGER.info("Introducing the assistant")

        response = await self.chat.chat("What is the best way to wake up in the morning?")
        LOGGER.info(f"Chat response: {response}")

        return response
