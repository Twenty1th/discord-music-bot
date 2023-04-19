from datetime import timedelta
from uuid import UUID

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from config import ACCESS_TOKEN_EXPIRE_MINUTES
from src.exceptions import UserEmailExists, PasswordMismatch, IncorrectFormData
from src.repository.repository import Repository
from src.services.api.auth.schema import UserAuthSchema, LoginResponse, UserLoginSchema
from src.services.api.settings import settings
from src.services.api.user.schema import UserInDB


class AuthController:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    SECRET_KEY = settings.auth_secret_key
    ALGORITHM = settings.algorithm
    TOKEN_TYPE = "bearer"

    def __init__(self, db: Repository):
        self.db = db

    async def create_user(self, form_data: UserAuthSchema) -> LoginResponse:
        email = form_data.email
        if self.get_user_by_email(email):
            raise UserEmailExists

        if form_data.password != form_data.password_confirm:
            raise PasswordMismatch

        hashed_password = self.get_password_hash(form_data.password)
        user: UserInDB = await self.db.create_user(UserInDB(username=email, hashed_password=hashed_password))
        access_token = self.create_token(user_email=user.email, user_uuid=user.uuid)
        response = {**user, "access_token": access_token, "token_type": "bearer"}
        return LoginResponse.parse_obj(response)

    async def get_token(self, form_data: UserLoginSchema) -> dict:
        user = await self.get_user_by_email(form_data.email)
        if not user:
            raise IncorrectFormData

        if not self.verify_password(form_password=form_data.password, user_hashed_password=user.hashed_password):
            raise IncorrectFormData

        token = self.create_token(form_data.email, user.uuid)
        return {"access_token": token, "token_type": self.TOKEN_TYPE}

    async def get_user_by_email(self, email: EmailStr) -> UserInDB:
        return await self.db.get_user_by_field(field="email", value=email)

    async def create_token(self, user_email: EmailStr, user_uuid: UUID) -> str:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        data = {"sub": user_email, 'uuid': user_uuid, "expires_delta": access_token_expires}
        encoded_jwt = jwt.encode(data, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    def verify_password(self, *, form_password: str, user_hashed_password: str) -> bool:
        return self.pwd_context.verify(form_password, user_hashed_password)

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def get_user_uuid_by_token(self, token: str) -> UUID:
        return jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM]).get("uuid")

    async def login_user(self, form_data: UserLoginSchema) -> dict:
        email: EmailStr = form_data.email
        if not (user := await self.get_user_by_email(email)):
            raise IncorrectFormData

        password = form_data.password
        if not self.verify_password(form_password=password, user_hashed_password=user.hashed_password):
            raise IncorrectFormData

        access_token = self.create_token(user.email, user_uuid=user.uuid)
        return {"access_token": access_token, "token_type": self.TOKEN_TYPE}
