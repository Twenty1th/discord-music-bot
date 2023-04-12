from typing import List, Dict, Type

from pydantic import BaseModel
from src.downloaders import Youtube

from config import DEFAULT_PATH, DEFAULT_MUSIC_FILE_EXTENSION
from src.services.download.modules.downloader import IDownloader


class DiscordConfig(BaseModel):
    token: str
    command_prefix: str


class DownloadersItem(BaseModel):
    name: str
    output_path: str = DEFAULT_PATH
    file_extension: str = DEFAULT_MUSIC_FILE_EXTENSION


class Config(BaseModel):
    discord: DiscordConfig
    downloaders: List[DownloadersItem]


class DownloadersList(BaseModel):
    members: Dict[str, Type[IDownloader]] = {
        "youtube": Youtube
    }
