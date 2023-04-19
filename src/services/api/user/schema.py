import time
from typing import List
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, EmailStr


class UserSchema(BaseModel):
    email: EmailStr
    discord_servers: List[int] = []
    discord_id: int = 0


class UserUpdateSchema(UserSchema):
    new_username: str


class UserInDB(UserSchema):
    uuid: UUID = Field(default_factory=uuid4)
    hashed_password: str
    created_time: int = Field(default_factory=time.time)
    last_login: int = Field(default_factory=time.time)

    class Config:
        orm_mode = True
