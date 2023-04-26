from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str
    app_version: str = "0.1.0"
    auth_secret_key: str
    algorithm: str
    db_username: str
    db_password: str
    db_host: str = "db_test"
    db_port: str = "5433"
    db_name: str = "test"
    repository_name: str
    access_token_expire_sec = 24 * 60 * 7  # One week

    class Config:
        env_file = ".env"

    @property
    def db_full_url(self):
        url = "postgresql+asyncpg://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
        return url.format(db_username=self.db_username,
                          db_password=self.db_password,
                          db_host=self.db_host,
                          db_port=self.db_port,
                          db_name=self.db_name)


@lru_cache()
def get_settings() -> Settings:
    return Settings()
