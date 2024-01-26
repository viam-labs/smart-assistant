import asyncio
from typing import Optional, Sequence

from viam.module.module import RobotClient
from viam.logging import getLogger

from chat_service_api import Chat
from speech_service_api import SpeechService

from .config import AssistantConfig

LOGGER = getLogger(__name__)

class Assistant:
    robot_client = RobotClient
    chat: Chat
    speech: SpeechService
    config: AssistantConfig

    def __init__(self, config: AssistantConfig):
        self.config = config

    async def close(self):
        if self.robot_client:
            await self.robot_client.close()

    async def start(self):
        LOGGER.info("Started assistant!")

        self.robot_client = await self.connect()
        self.chat = Chat.from_robot(self.robot_client, self.config.chat_name)
        self.speech = SpeechService.from_robot(self.robot_client, self.config.speech_name)

        await self.speech.listen_trigger(type="command")
        await self.speech.say("Hello from your Viam smart assistant! How can I help you today?", blocking=False)

        LOGGER.info("Waiting for command.")
        command = await self.handle_commands()
        await self.speech.say(f"I've received the command: {command}. Working on that now.", blocking=False)
        response = await self.chat.chat(message=command)
        await self.speech.say(f"Thanks for waiting! {response}", blocking=True)

        await self.close()

    async def connect(self):
        opt = RobotClient.Options.with_api_key(api_key=self.config.api_key, api_key_id=self.config.api_key_id)
        return await RobotClient.at_address(self.config.address, opt)

    async def handle_commands(self):
        commands: Optional[Sequence[str]] = None
        while commands == None:
            commands = await self.speech.get_commands(1)
            if len(commands) > 0:
                LOGGER.debug(f"Commands: {commands}")
            else:
                commands = None
                await asyncio.sleep(1)

        return commands[0]
