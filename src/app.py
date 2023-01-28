import asyncio
import tomllib

import discord

from src.discord import Bot, MusicCommands
from src.downloaders import Youtube
from src.models import Config


class Application:

    def __init__(self):
        with open('config.toml', 'rb') as f:
            self.config_data: Config = Config.parse_obj(tomllib.load(f))

    async def __init_discord_bot(self):
        intents = discord.Intents.default()
        intents.message_content = True
        bot = Bot(intents=intents, command_prefix="!")
        cog = MusicCommands(bot=bot)
        bot.loop = asyncio.get_event_loop()
        await bot.add_cog(cog)
        bot.run(self.config_data.discord.token)

    def run(self):
        asyncio.run(self.__init_discord_bot())  # TODO
