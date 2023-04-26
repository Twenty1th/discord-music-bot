import asyncio
from typing import Any

from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from src.repository.repository import Repository
from src.services.api.user.schema import User, UserID
from src.settings import get_settings

settings = get_settings()


class Postgres(Repository):
    async_session: AsyncSession
    db_full_url = "postgresql+asyncpg://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
    print(settings.db_name)

    def __init__(self):
        self.engine = create_async_engine(settings.db_full_url,
                                          future=True,
                                          echo=True)

    async def get_user_by_field(self, *, field: str, value: Any) -> User:
        query = select(User).where(getattr(User, field) == value)
        res = await self.async_session.execute(query)
        user_row: User = res.scalar()
        return user_row

    async def create_user(self, user: User) -> User:
        new_user = User(**user.dict())
        self.async_session.add(new_user)
        await self.async_session.flush()
        await self.async_session.commit()
        return User(email=new_user.email,
                    id=new_user.id,
                    discord_id=new_user.discord_id,
                    hashed_password=new_user.hashed_password,
                    created_time=new_user.created_time,
                    last_login=new_user.last_login
                    )

    async def update_user(self, *, search_field: str, search_value: Any, **kwargs) -> User:
        query = update(User).where(getattr(User, search_field) == search_value).values(kwargs)
        await self.async_session.execute(query)
        await self.async_session.commit()
        return User.parse_obj(kwargs)

    async def delete_user(self, uuid: UserID) -> UserID:
        pass

    async def __run_engine(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    async def connect(self):
        asyncio.create_task(self.__run_engine())
        self.async_session = sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)()  # noqa

    async def disconnect(self):
        await self.async_session.close()
