from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    # API
    app_name: str = "Backend API"
    api_version: str = "0.1.0"
    api_port: int = 8080
    workers: int = 1
    repository_name: str

    # Security
    auth_secret_key: str
    algorithm: str
    access_token_expire_sec = 24 * 60 * 7  # One week
    TOKEN_TYPE: str

    # Database
    db_username: str
    db_password: str
    db_host: str = "db_test"
    db_port: str = "5433"
    db_name: str = "test"

    # Discord
    API_ENDPOINT: str
    API_USER_INFO_ENDPOINT = 'https://discordapp.com/api/users/@me'
    REDIRECT_URI = 'http://localhost:8080/api_v1/oauth2/auth'
    CLIENT_ID: str
    CLIENT_SECRET: str
    GRANT_TYPE: str
    OAUTH2_URL: str

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
