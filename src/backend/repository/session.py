from typing import Dict

from core.settings import get_settings
from repository.memory.memory import MemoryDB
from repository.postgres.postgres import Postgres
from repository.repository import Repository

settings = get_settings()


async def get_db() -> Repository:
    dbs: Dict[str, Repository] = {
        "dictionary": MemoryDB(),
        "postgres": Postgres()
    }
    db = dbs[settings.repository_name.strip()]
    await db.connect()
    try:
        yield db

    finally:
        await db.disconnect()
