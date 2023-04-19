from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

from src.services.api.user.schema import UserInDB, UserUpdateSchema


class Repository(ABC):

    @abstractmethod
    async def get_user_by_field(self, *, field: str, value: Any) -> UserInDB:
        pass

    @abstractmethod
    async def create_user(self, user: UserInDB) -> UserInDB:
        pass

    @abstractmethod
    async def update_user(self, new_user: UserUpdateSchema) -> UserInDB:
        pass

    @abstractmethod
    async def delete_user(self, uuid: UUID) -> UUID:
        pass

    @abstractmethod
    async def connect(self):
        pass

    @abstractmethod
    async def disconnect(self):
        pass
