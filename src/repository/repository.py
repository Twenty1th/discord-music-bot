from abc import ABC, abstractmethod
from typing import Any

from src.services.api.user.schema import User


class Repository(ABC):

    @abstractmethod
    async def get_user_by_field(self, *, field: str, value: Any) -> User:
        pass

    @abstractmethod
    async def create_user(self, user: User) -> User:
        pass

    @abstractmethod
    async def update_user(self, *, search_field: str, search_value: Any, **kwargs) -> User:
        pass

    @abstractmethod
    async def delete_user(self, uuid: int) -> int:
        pass

    @abstractmethod
    async def connect(self):
        pass

    @abstractmethod
    async def disconnect(self):
        pass
