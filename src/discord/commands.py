import logging

import discord
from discord import VoiceChannel
from discord.ext.commands import Context
from discord.ext import commands

from src.discord import Bot


class MusicCommands(commands.Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    def __get_link_from_message(cxt: Context) -> str:
        message = cxt.message
        logging.info(message)
        return message.content.split(" ")[-1]

    @commands.command()
    async def play(self, ctx: Context):
        if not self.bot.bot_is_connected_to_voice_channel():
            channel: VoiceChannel = self.bot.find_channel_with_author(ctx)
            self.bot.init_voice_client(channel)
            await self.bot.connect_to_voice_channel()
        link: str = self.__get_link_from_message(ctx)
        path = await self.downloader.get_path_to_music_file_by_link(link)
        self.bot.voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg-5.1.2-essentials_build/bin/ffmpeg.exe", source=path))

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
