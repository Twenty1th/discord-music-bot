import logging

import discord
from discord import VoiceChannel
from discord.ext.commands import Context
from discord.ext import commands

from src.downloaders.downloader import DownloaderInterface


class MusicCommands(commands.Cog):
    voice_client: discord.VoiceClient = None

    def __init__(self, downloader: DownloaderInterface):
        self.downloader = downloader

    def __bot_connected_to_voice_channel(self, voice_channel: VoiceChannel) -> bool:
        return self.voice_client.channel.name == voice_channel.name

    @staticmethod
    def __find_user_in_channels(ctx: Context) -> VoiceChannel | None:
        for voice_channel in ctx.guild.voice_channels:
            if ctx.author.name in [member.name for member in voice_channel.members]:
                logging.info(f"Voice channel: {voice_channel}")
                return voice_channel
        else:
            logging.error("Voice channel is not found")
            return None

    def __voice_client_is_init(self) -> bool:
        return self.voice_client is not None

    async def __connect_bot_to_voice_channel(self, voice_channel: VoiceChannel):
        if not self.__voice_client_is_init() or not self.__bot_connected_to_voice_channel(voice_channel):
            logging.info(f"Bot connected to {voice_channel.name}")
            self.voice_client = await voice_channel.connect()

    @staticmethod
    def __get_link_from_message(cxt: Context) -> str:
        message = cxt.message
        logging.info(message)
        return message.content.split(" ")[-1]

    @commands.command()
    async def play(self, ctx: Context):
        voice_channel = self.__find_user_in_channels(ctx)
        if voice_channel:
            await self.__connect_bot_to_voice_channel(voice_channel)
            if not self.voice_client.is_playing():
                link = self.__get_link_from_message(ctx)
                path = await self.downloader.download(link)
                self.voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg-5.1.2-essentials_build/bin/ffmpeg.exe",
                                                              source=path))

    @commands.command()
    async def stop(self, ctx: Context):
        self.voice_client.stop()

    @commands.command()
    async def pause(self, ctx: Context):
        self.voice_client.pause()

    @commands.command()
    async def resume(self, ctx: Context):
        self.voice_client.resume()
