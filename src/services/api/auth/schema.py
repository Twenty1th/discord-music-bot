from typing import Optional

from fastapi import Form
from pydantic import BaseModel, EmailStr


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


class MyForm:
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
