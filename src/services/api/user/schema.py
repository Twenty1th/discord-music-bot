import time
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, EmailStr


class User(BaseModel):
    username: str
    email: EmailStr


class UserBaseSchema(User):
    uuid: UUID = Field(default_factory=uuid4)
    hashed_password: str
    created_time: int = Field(default_factory=time.time)
    last_login: int = Field(default_factory=time.time)

    class Config:
        orm_mode = True
