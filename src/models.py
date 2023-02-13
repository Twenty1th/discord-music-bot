from typing import List, Dict, Type

from pydantic import BaseModel

from src.downloaders import Youtube
from src.downloaders.downloader import DownloaderInterface


class DiscordConfig(BaseModel):
    token: str
    command_prefix: str


class DownloadersItem(BaseModel):
    name: str
    output_path: str
    file_extension: str


class Config(BaseModel):
    discord: DiscordConfig
    downloaders: List[DownloadersItem]


class DownloadersList(BaseModel):
    members: Dict[str, Type[DownloaderInterface]] = {
            "youtube": Youtube
        }
