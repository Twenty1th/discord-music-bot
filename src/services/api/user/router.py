from fastapi import APIRouter, HTTPException, Depends
from starlette import status

from src.repository.models import get_db
from src.services.api.user.controller import UserController
from src.services.api.user.helpers import get_email_by_token
from src.services.api.user.schema import UserSchema, UserUpdateSchema

router = APIRouter(
    prefix="/profile"
)

controller = UserController(db=Depends(get_db))


@router.post("/", response_model=UserSchema)
async def get_profile_info(token: str | None):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not (email := get_email_by_token(token)):
        raise credentials_exception

    user = await controller.get_user_by_email(email)
    return user


@router.post("/update", response_model=UserSchema)
async def update_profile(form_data: UserUpdateSchema):
    new_user_profile: UserSchema = await controller.update_user(form_data)
    return new_user_profile
