import logging

from discord import VoiceChannel, VoiceClient
from discord.ext import commands
from discord.ext.commands import Context


class BotVoiceClient(VoiceClient):
    pass


class Bot(commands.Bot):
    __voice_client: BotVoiceClient = None

    def init_voice_client(self, channel: VoiceChannel):
        voice_client = BotVoiceClient(self, channel)
        self.__voice_client = voice_client

    @property
    def voice_client(self) -> BotVoiceClient:
        if self.__voice_client is None:
            raise  # TODO
        return self.__voice_client

    def bot_is_connected_to_voice_channel(self):
        return self.__voice_client.is_connected()

    async def connect_to_voice_channel(self):
        if not self.__voice_client.is_connected():
            await self.__voice_client.voice_connect()

    async def disconnect_from_channel(self):
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
