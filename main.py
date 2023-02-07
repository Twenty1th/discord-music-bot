import asyncio
import tomllib

from src.app import Application
from src.downloaders import Youtube
from src.models import Config

if __name__ == '__main__':
    with open('config.toml', 'rb') as f:
        print(tomllib.load(f))
        config: Config = Config.parse_obj(tomllib.load(f))
    print(config)

    youtube_downloader = Youtube(output_path=config.downloaders['youtube'].output_path,
                                 file_extension=config.downloaders['youtube'].file_extension)

    app = Application()
    app.add_downloader(youtube_downloader)
    loop = asyncio.new_event_loop()
    loop.run_until_complete(app.init_discord_bot(command_prefix=config.discord.command_prefix,
                                                 token=config.discord.token))
    loop.run_until_complete(app.run())
