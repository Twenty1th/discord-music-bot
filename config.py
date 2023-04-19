from pathlib import Path
from typing import List

DEFAULT_PATH: str = str(Path().resolve())
DEFAULT_PATH_TO_DOWNLOADERS_MODULES: str = f"src.services.download.modules"
DEFAULT_MUSIC_FILE_EXTENSION: str = "mp3"
LIST_OF_MUSIC_SERVICES: List[str] = ['youtube']

ACCESS_TOKEN_EXPIRE_MINUTES = 24 * 60 * 7  # One week

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
