from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status, APIRouter

from config import ACCESS_TOKEN_EXPIRE_MINUTES
from src.services.api.auth.heplers import authenticate_user, create_access_token, \
    fake_users_db, get_password_hash, add_user_to_database
from src.services.api.auth.schema import Token, UserLoginSchema, UserAuthSchema
from src.services.api.user.schema import UserBaseSchema

router = APIRouter(
    prefix="/auth"
)


@router.post("")
async def authentication(form_data: Annotated[UserAuthSchema, Depends()]):
    email = form_data.email
    if email in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User with this email is exists. Try again with other email",
        )
    if form_data.password != form_data.password_confirm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password mismatch"
        )
    hashed_password = get_password_hash(form_data.password)
    user_in_db: UserBaseSchema = UserBaseSchema(username=email, hashed_password=hashed_password)
    add_user_to_database(user=user_in_db)
    access_token = create_access_token(data={"sub": email, 'uuid': user_in_db.uuid})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/token", response_model=Token)
async def get_access_token(form_data: Annotated[UserLoginSchema, Depends()]):
    user = authenticate_user(fake_users_db, form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, 'uuid': user.uuid}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
async def login(form_data: Annotated[UserLoginSchema, Depends()]):
    email = form_data.email
    if email not in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User with this email is not exists",
        )
    password = form_data.password
    user = authenticate_user(fake_users_db, email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username, 'uuid': user.uuid})
    return {"access_token": access_token, "token_type": "bearer"}
