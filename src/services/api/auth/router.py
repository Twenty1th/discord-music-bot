from typing import Annotated

from fastapi import Depends, APIRouter, Response

from src.repository.database import get_db
from src.repository.repository import Repository
from src.services.api.auth.controller import AuthController
from src.services.api.auth.schema import Token, UserAuthSchema, MyForm
from src.settings import get_settings

router = APIRouter(
    prefix=""
)

settings = get_settings()


@router.post("/auth", response_model=Token)
async def authentication(form_data: Annotated[UserAuthSchema, Depends()],
                         db: Repository = Depends(get_db)):
    controller: AuthController = AuthController(db=db)
    login_data = await controller.create_user(form_data)
    return login_data


@router.post("/login", response_model=Token)
async def login(form_data: Annotated[MyForm, Depends()],
                response: Response,
                db: Repository = Depends(get_db)):
    controller: AuthController = AuthController(db=db)
    login_data: Token = await controller.login_user(form_data)
    response.set_cookie(key='token', value=login_data.access_token,
                        expires=settings.access_token_expire_sec, httponly=True)
    response.headers['token'] = login_data.access_token
    return login_data
