import logging
from typing import Dict
from urllib.parse import urlparse

from discord import VoiceChannel
from discord.ext import commands
from discord.ext.commands import Context

from src.exceptions import UnknownLink
from src.services.discord import Bot
from src.services.download.modules.downloader import IDownloader


class MusicCommands(commands.Cog):

    def __init__(self, bot: Bot, downloaders: Dict[str, IDownloader]):
        self.bot = bot
        self.__downloaders: Dict[str, IDownloader] = downloaders

    @staticmethod
    def __get_link_from_message(cxt: Context) -> str:
        message = cxt.message
        logging.info(message)
        return message.content.split(" ")[-1]

    @staticmethod
    def __get_service_name_by_link(link: str) -> str:
        match urlparse(link).netloc:
            case "www.youtube.com" | "youtube.com":
                return "youtube"

            case _:
                raise UnknownLink(f"Unknown link {link}")

    @commands.command()
    async def play(self, ctx: Context):
        if not self.bot.is_connected_to_voice_channel():
            channel: VoiceChannel = self.bot.find_channel_with_author(ctx)
            await self.bot.init_voice_client(channel)
            await self.bot.connect_to_voice_channel()

        if self.bot.voice_client.is_playing():
            self.bot.voice_client.stop()

        link: str = self.__get_link_from_message(ctx)
        service_name = self.__get_service_name_by_link(link)
        path: str = await self.__downloaders[service_name].download(link)
        self.bot.play(path)

    @commands.command()
    async def stop(self, ctx: Context):
        if self.bot.voice_client.is_playing():
            self.bot.voice_client.stop()

    @commands.command()
    async def pause(self, ctx: Context):
        if self.bot.voice_client.is_playing():
            self.bot.voice_client.pause()

    @commands.command()
    async def resume(self, ctx: Context):
        if not self.bot.voice_client.is_playing():
            self.bot.voice_client.resume()
