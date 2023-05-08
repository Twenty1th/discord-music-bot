from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from api_v1.schemas import UserInfo, UserUpdateSchema
from api_v1.user.controller import UserController
from repository.repository import Repository
from repository.session import get_db

router = APIRouter(
    prefix=""
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api_v1/v1/auth/login",
                                     scheme_name="JWT")

db: Repository = Depends(get_db)
controller = UserController(db=db)


@router.post("/", response_model=UserInfo)
async def get_profile_info(token: Annotated[str, Depends(oauth2_scheme)]):
    user = await controller.get_user(token)
    return user


@router.post("/update", response_model=UserInfo)
async def update_profile(token: Annotated[str, Depends(oauth2_scheme)],
                         form_data: UserUpdateSchema):
    new_user_profile: UserInfo = await controller.update_user(form_data, token)
    return new_user_profile
