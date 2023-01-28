from pydantic import BaseModel


class DiscordConfig(BaseModel):
    token: str


class Config(BaseModel):
    discord: DiscordConfig
