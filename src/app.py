import asyncio
from typing import Dict

import discord

from src.discord import Bot, MusicCommands
from src.downloaders.downloader import DownloaderInterface
from src.exceptions import DiscordBotIsNotInit


class Application:
    __downloaders: Dict[str, DownloaderInterface] = {}
    __bot: Bot = None

    def add_downloader(self, name: str, instance: DownloaderInterface) -> None:
        self.__downloaders[name] = instance

    async def init_discord_bot(self, *, command_prefix: str, token: str) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        self.__bot = Bot(intents=intents, command_prefix=command_prefix, token=token)
        cog = MusicCommands(bot=self.__bot, downloaders=self.__downloaders)
        self.__bot.loop = asyncio.get_event_loop()
        await self.__bot.add_cog(cog)

    def run(self):
        if self.__bot is None:
            raise DiscordBotIsNotInit("Discord bot is not initial. Use init_discord_bot method")
        self.__bot.run(token=self.__bot.token)
