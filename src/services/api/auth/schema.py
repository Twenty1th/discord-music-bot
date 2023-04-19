from pydantic import BaseModel, EmailStr

from src.services.api.user.schema import UserSchema


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


class LoginResponse(Token, UserSchema):
    email: EmailStr
