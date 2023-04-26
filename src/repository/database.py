from typing import Dict

from src.repository.postgres.postgres import Postgres
from src.repository.repository import Repository
from src.repository.test_db.test_db import TestDB
from src.settings import get_settings

settings = get_settings()


async def get_db() -> Repository:
    dbs: Dict[str, Repository] = {
        "dictionary": TestDB(),
        "postgres": Postgres()
    }
    db = dbs[settings.repository_name.strip()]
    await db.connect()
    try:
        yield db

    finally:
        await db.disconnect()
