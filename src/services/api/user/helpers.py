from fastapi import HTTPException
from jose import JWTError, jwt
from pydantic import EmailStr
from starlette import status


async def get_user_info(email: EmailStr):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = get_user(fake_users_db, username=username)
    if user is None:
        raise credentials_exception
    return user


def get_email_by_token(token: str) -> EmailStr | str:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]).get('sub')
    except JWTError:
        return ""
