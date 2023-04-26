from datetime import timedelta

from jose import jwt, JWTError
from pydantic import EmailStr

from src.services.api.exceptions import Unauthorized
from src.services.api.user.schema import UserID
from src.settings import get_settings

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
