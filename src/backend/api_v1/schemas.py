import time
from typing import NewType
from typing import Optional
from uuid import uuid1

from fastapi import Form
from pydantic import EmailStr, BaseModel
from sqlalchemy import Column, BigInteger
from sqlmodel import SQLModel, Field


class UserAuthSchema(BaseModel):
    email: EmailStr
    password: str
    password_confirm: str


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class LoginForm:
    def __init__(self, grant_type: str = Form(default=None, regex="password"),
                 email=Form(),
                 password: str = Form(), scope: str = Form(default=""), client_id: Optional[str] = Form(default=None),
                 client_secret: Optional[str] = Form(default=None)):
        self.email: EmailStr = email
        self.grant_type = grant_type
        self.password = password
        self.scopes = scope.split()
        self.client_id = client_id
        self.client_secret = client_secret


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


class DiscordOAuth(BaseModel):
    access_token: str
    expires_in: str
    refresh_token: str
    scope: str
    token_type: str
