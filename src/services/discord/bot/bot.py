import logging
from typing import Any

import discord
from discord import VoiceChannel, VoiceClient
from discord.ext import commands
from discord.ext.commands import Context


class BotVoiceClient(VoiceClient):
    pass


class Bot(commands.Bot):
    __voice_client: BotVoiceClient = None

    def __init__(self, command_prefix, *, intents: discord.Intents, token: str, **options: Any):
        super().__init__(command_prefix, intents=intents, **options)
        self.token = token

    async def init_voice_client(self, channel: VoiceChannel) -> None:
        self.__voice_client = await channel.connect()

    @property
    def voice_client(self) -> BotVoiceClient:
        if self.__voice_client is None:
            raise  # TODO
        return self.__voice_client

    def is_connected_to_voice_channel(self) -> bool:
        if self.__voice_client is None:
            return False
        return self.__voice_client.is_connected()

    async def connect_to_voice_channel(self) -> None:
        if not self.voice_client.is_connected():
            await self.__voice_client.channel.connect()

    async def disconnect_from_channel(self) -> None:
        if self.__voice_client.is_connected():
            await self.__voice_client.disconnect()

    @staticmethod
    def find_channel_with_author(ctx: Context) -> VoiceChannel | None:
        for voice_channel in ctx.guild.voice_channels:
            if ctx.author.name in [member.name for member in voice_channel.members]:
                logging.info(f"Voice channel: {voice_channel}")
                return voice_channel
        else:
            logging.error("Voice channel is not found")
            return None

    @staticmethod
    def __get_link_from_message(cxt: Context) -> str:
        message = cxt.message
        logging.info(message)
        return message.content.split(" ")[-1]

    def play(self, path: str):
        self.voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg-5.1.2-essentials_build/bin/ffmpeg.exe",
                                                        source=path))
