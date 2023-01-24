import asyncio
import tomllib
import discord

from src.discord import Bot, MusicCommands
from src.downloaders import Youtube

if __name__ == '__main__':
    with open('config.toml', 'rb') as f:
        data = tomllib.load(f)

    intents = discord.Intents.default()
    intents.message_content = True
    client = Bot(intents=intents, command_prefix="!")
    asyncio.run(client.add_cog(MusicCommands(downloader=Youtube())))
    client.run(data['discord']['token'])
