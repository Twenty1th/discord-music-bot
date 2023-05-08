from datetime import timedelta

from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import EmailStr

from api_v1.schemas import UserID
from core.exceptions import Unauthorized
from core.settings import get_settings

settings = get_settings()


async def create_token(user_email: EmailStr, user_uuid: UserID, **kwargs) -> str:
    data = {"sub": user_email, 'id': user_uuid, **kwargs,
            "expires_delta": timedelta(minutes=settings.access_token_expire_sec).seconds}
    encoded_jwt = jwt.encode(data, settings.auth_secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def get_user_field_from_token(*, field: str, token: str) -> UserID:
    try:
        if not (field := jwt.decode(token, settings.auth_secret_key, algorithms=[settings.algorithm]).get(field)):
            raise Unauthorized
        return field
    except JWTError:
        raise Unauthorized


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(*, form_password: str, user_hashed_password: str) -> bool:
    return pwd_context.verify(form_password, user_hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
