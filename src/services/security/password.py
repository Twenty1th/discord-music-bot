from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(*, form_password: str, user_hashed_password: str) -> bool:
    return pwd_context.verify(form_password, user_hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
