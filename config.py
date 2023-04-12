from pathlib import Path
from typing import List

DEFAULT_PATH: str = str(Path().resolve())
DEFAULT_PATH_TO_DOWNLOADERS_MODULES: str = f"src.services.download.modules"
DEFAULT_MUSIC_FILE_EXTENSION: str = "mp3"
LIST_OF_MUSIC_SERVICES: List[str] = ['youtube']

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
