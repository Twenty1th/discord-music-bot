from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str
    app_version: str = "0.1.0"
    db_full_url: str
    auth_secret_key: str
    algorithm: str

    class Config:
        env_file = ".env"


settings = Settings()
