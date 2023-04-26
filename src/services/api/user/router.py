from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from src.repository.database import get_db
from src.repository.repository import Repository
from src.services.api.user.controller import UserController
from src.services.api.user.schema import UserInfo, UserUpdateSchema

router = APIRouter(
    prefix=""
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login",
                                     scheme_name="JWT")


@router.post("/", response_model=UserInfo)
async def get_profile_info(token: Annotated[str, Depends(oauth2_scheme)], db: Repository = Depends(get_db)):
    controller = UserController(db=db)
    user = await controller.get_user(token)
    return user


@router.post("/update", response_model=UserInfo)
async def update_profile(token: Annotated[str, Depends(oauth2_scheme)],
                         form_data: UserUpdateSchema,
                         db: Repository = Depends(get_db)):
    controller = UserController(db=db)
    new_user_profile: UserInfo = await controller.update_user(form_data, token)
    return new_user_profile
