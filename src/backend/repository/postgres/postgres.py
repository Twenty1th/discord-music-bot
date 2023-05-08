from typing import Any

from sqlalchemy import update, select, delete
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from api_v1.schemas import User, UserID
from core.settings import get_settings
from repository.repository import Repository

settings = get_settings()


class Postgres(Repository):
    db_full_url = "postgresql+asyncpg://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"

    def __init__(self):
        self.engine = create_async_engine(settings.db_full_url,
                                          future=True,
                                          echo=False)
        self.session_fabric = sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession,
                                           autoflush=True)

    async def get_user_by_field(self, *, field: str, value: Any) -> User:
        async with self.session_fabric() as session:
            session: AsyncSession
            query = select(User).where(getattr(User, field) == value)
            res = await session.execute(query)
            user: User = res.scalar()
            return user

    async def create_user(self, user: User) -> User:
        async with self.session_fabric() as session:
            session: AsyncSession
            new_user = User(**user.dict())
            session.add(new_user)
            await session.commit()
            user = await self.get_user_by_field(field="email", value=new_user.email)
            return user

    async def update_user(self, *, search_field: str, search_value: Any, **kwargs) -> User:
        async with self.session_fabric() as session:
            query = update(User).where(getattr(User, search_field) == search_value).values(kwargs)
            await session.execute(query)
            await session.commit()
            return User.parse_obj(kwargs)

    async def delete_user(self, uuid: UserID) -> UserID:
        async with self.session_fabric() as session:
            query = delete(User).where(User.id == UserID)
            await session.execute(query)
            await session.commit()
            return True

    async def connect(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    async def disconnect(self):
        self.session_fabric.close_all()
