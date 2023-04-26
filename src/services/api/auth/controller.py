from pydantic import EmailStr

from src.repository.repository import Repository
from src.services.api.auth.schema import UserAuthSchema, Token, MyForm
from src.services.api.exceptions import UserEmailExists, PasswordMismatch, IncorrectFormData
from src.services.api.user.schema import User
from src.services.security.jwt import create_token
from src.services.security.password import get_password_hash, verify_password
from src.settings import get_settings

settings = get_settings()


class AuthController:
    SECRET_KEY = settings.auth_secret_key
    ALGORITHM = settings.algorithm
    TOKEN_EXPIRE = settings.access_token_expire_sec
    TOKEN_TYPE = "bearer"

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

    async def login_user(self, form_data: MyForm) -> Token:
        email: EmailStr = form_data.email
        if not (user := await self.db.get_user_by_field(field="email", value=email)):
            raise IncorrectFormData

        password = form_data.password
        if not verify_password(form_password=password, user_hashed_password=user.hashed_password):
            raise IncorrectFormData

        access_token = await create_token(user.email, user_uuid=user.id)
        return Token(access_token=access_token, token_type="bearer")
