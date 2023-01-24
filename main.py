import asyncio
import tomllib
import discord

from src.discord.bot import MyClient, GreetingsVoice
from src.downloader import Youtube

if __name__ == '__main__':
    with open('config.toml', 'rb') as f:
        data = tomllib.load(f)

    intents = discord.Intents.default()
    intents.message_content = True
    client = MyClient(intents=intents, command_prefix="!")
    asyncio.run(client.add_cog(GreetingsVoice(downloader=Youtube())))
    client.run(data['discord']['token'])
