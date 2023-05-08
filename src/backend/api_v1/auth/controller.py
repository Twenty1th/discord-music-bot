from typing import Dict

import httpx as httpx
from pydantic import EmailStr

from api_v1.schemas import User
from api_v1.schemas import UserAuthSchema, Token, LoginForm, DiscordOAuth
from core.exceptions import UserEmailExists, PasswordMismatch, IncorrectFormData
from core.security import get_password_hash, create_token, verify_password
from core.settings import get_settings
from repository.repository import Repository

settings = get_settings()


class AuthController:
    SECRET_KEY = settings.auth_secret_key
    ALGORITHM = settings.algorithm
    TOKEN_EXPIRE = settings.access_token_expire_sec
    TOKEN_TYPE = settings.TOKEN_TYPE

    def __init__(self, db: Repository):
        self.db = db

    async def create_user(self, form_data: UserAuthSchema) -> Token:
        email = form_data.email
        if await self.db.get_user_by_field(field="email", value=email):
            raise UserEmailExists

        if form_data.password != form_data.password_confirm:
            raise PasswordMismatch

        hashed_password = get_password_hash(form_data.password)
        user: User = await self.db.create_user(User(email=email, hashed_password=hashed_password))
        access_token = await create_token(user_email=user.email,
                                          user_uuid=user.id,
                                          discord_id=user.discord_id)
        return Token(access_token=access_token, token_type="bearer")

    async def login_user(self, form_data: LoginForm) -> Token:
        email: EmailStr = form_data.email
        if not (user := await self.db.get_user_by_field(field="email", value=email)):
            raise IncorrectFormData

        password = form_data.password
        if not verify_password(form_password=password, user_hashed_password=user.hashed_password):
            raise IncorrectFormData

        access_token = await create_token(user.email, user_uuid=user.id)
        return Token(access_token=access_token, token_type="bearer")

    @staticmethod
    async def auth_discord(code: str) -> DiscordOAuth:
        data = {
            'client_id': settings.CLIENT_ID,
            'client_secret': settings.CLIENT_SECRET,
            'grant_type': settings.GRANT_TYPE,
            'code': code,
            'redirect_uri': settings.REDIRECT_URI
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        async with httpx.AsyncClient() as client:
            r = await client.post('%s' % settings.API_ENDPOINT, data=data, headers=headers)
            return DiscordOAuth.parse_obj(r.json())

    @staticmethod
    async def login_discord(credentials: DiscordOAuth) -> Dict:
        headers = {
            'Authorization': '{} {}'.format(credentials.token_type, credentials.access_token)
        }
        async with httpx.AsyncClient() as client:
            r = await client.post('%s' % settings.API_USER_INFO_ENDPOINT, headers=headers)
            return r.json()
