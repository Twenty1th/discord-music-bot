from typing import Dict

from src.repository.repository import Repository
from test_db.test_db import TestDB


async def get_db(db_name: str) -> Repository:
    dbs: Dict[str, Repository] = {
        "Dictionary": TestDB(),
        "Postgres": None
    }
    db = dbs[db_name]
    await db.connect()
    try:
        yield db
    finally:
        await db.disconnect()
