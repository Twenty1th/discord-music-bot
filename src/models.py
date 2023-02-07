from typing import Dict

from pydantic import BaseModel

from src.enums import DownloadersList


class DiscordConfig(BaseModel):
    token: str
    command_prefix: str


class DownloadersItem:
    output_path: str
    file_extension: str


class Config(BaseModel):
    discord: DiscordConfig
    downloaders: Dict
