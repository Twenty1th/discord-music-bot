from typing import Annotated

from fastapi import Depends, APIRouter, Response

from config import ACCESS_TOKEN_EXPIRE_MINUTES
from src.repository.models import get_db
from src.services.api.auth.controller import AuthController
from src.services.api.auth.schema import Token, UserLoginSchema, UserAuthSchema, LoginResponse

router = APIRouter(
    prefix=""
)

controller: AuthController = AuthController(db=Depends(get_db))


@router.post("/auth", response_model=LoginResponse)
async def authentication(form_data: Annotated[UserAuthSchema, Depends()]):
    response = controller.create_user(form_data)
    return response


@router.post("/token", response_model=Token)
async def get_access_token(form_data: Annotated[UserLoginSchema, Depends()]):
    token_data: dict = await controller.get_token(form_data)
    return token_data


@router.post("/login", response_model=Token)
async def login(form_data: Annotated[UserLoginSchema, Depends()], response: Response):
    login_data: dict = await controller.login_user(form_data)
    response.set_cookie(key='token', value=login_data['access_token'],
                        expires=ACCESS_TOKEN_EXPIRE_MINUTES, httponly=True)
    return login_data
