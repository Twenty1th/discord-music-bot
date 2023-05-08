import asyncio
from typing import Dict

import discord

from core.exceptions import DiscordBotIsNotInit
from src.backend.api_v1 import API
# from backend.services.discord import Bot, MusicCommands
from src.services.download.modules.downloader import IDownloader


class Application:
    __downloaders: Dict[str, IDownloader] = {}
    __bot: Bot = None
    __api_service: API = None

    def add_downloader(self, name: str, instance: IDownloader) -> None:
        self.__downloaders[name] = instance

    async def init_discord_bot(self, *, command_prefix: str, token: str) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        self.__bot = Bot(intents=intents, command_prefix=command_prefix, token=token)
        cog = MusicCommands(bot=self.__bot, downloaders=self.__downloaders)
        self.__bot.loop = asyncio.get_event_loop()
        await self.__bot.add_cog(cog)

    async def init_api_service(self, api_service: API):
        self.__api_service = api_service

    async def start_api_service(self):
        self.__api_service.start()

    async def start_discord_bot(self):
        pass

    def run(self):
        if self.__bot is None:
            raise DiscordBotIsNotInit("Discord bot is not initial. Use init_discord_bot method")
        self.__bot.run(token=self.__bot.token)
