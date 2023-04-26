import time
from typing import NewType
from uuid import uuid1

from pydantic import EmailStr, BaseModel
from sqlalchemy import Column, BigInteger
from sqlmodel import SQLModel, Field

UserID = NewType("UserID", int)


class UserInfo(SQLModel):
    email: EmailStr = Field(unique=True, index=True, alias="email")
    discord_id: int = 0


class User(UserInfo, table=True):
    id: UserID = Field(default_factory=lambda: uuid1().time_mid, alias="id",
                       sa_column=Column(BigInteger(), primary_key=True, index=True))
    hashed_password: str
    created_time: int = Field(default_factory=time.time)
    last_login: int = Field(default_factory=time.time)


class UserUpdateSchema(BaseModel):
    new_email: EmailStr
    # discord_servers: List[int] = [] # TODO
    new_discord_id: int = 0
