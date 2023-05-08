from typing import Any
from uuid import UUID

from api_v1.schemas import User
from repository.repository import Repository


class MemoryDB(Repository):
    async def update_user(self, *, search_field: str, search_value: Any, **kwargs) -> User:
        pass

    async def get_user_by_field(self, *, field: str, value: Any) -> User:
        pass

    async def connect(self):
        pass

    async def disconnect(self):
        pass

    fake_users_db = {
        "johndoe": {
            "username": "johndoe",
            "full_name": "John Doe",
            "email": "johndoe@example.com",
            "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
            "discord_id": 0,
            "discord_servers": []
        }
    }

    def get_user(self, uuid: UUID):
        pass

    def create_user(self, user: User):
        pass

    def delete_user(self, uuid: UUID):
        pass
