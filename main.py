import asyncio
import tomllib

from src.app import Application
from src.models import Config, DownloadersList

if __name__ == '__main__':
    with open('config.toml', 'rb') as f:
        config: Config = Config.parse_obj(tomllib.load(f))
    app = Application()
    downloaders_list = DownloadersList()
    for downloader in config.downloaders:
        instance = downloaders_list.members[downloader.name](file_extension=downloader.file_extension,
                                                             output_path=downloader.output_path)
        name = downloader.name
        app.add_downloader(name=name, instance=instance)
    loop = asyncio.new_event_loop()
    loop.run_until_complete(app.init_discord_bot(command_prefix=config.discord.command_prefix,
                                                 token=config.discord.token))
    loop.run_until_complete(app.run())
