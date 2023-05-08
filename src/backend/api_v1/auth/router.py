from typing import Annotated

from fastapi import Depends, APIRouter, Response

from api_v1.auth.controller import AuthController
from api_v1.schemas import Token, UserAuthSchema, LoginForm, DiscordOAuth
from core.settings import get_settings
from repository.repository import Repository
from repository.session import get_db

router = APIRouter(
    prefix=""
)

settings = get_settings()

db: Repository = Depends(get_db)
controller: AuthController = AuthController(db=db)


@router.post("/auth", response_model=Token, description="Authenticate by JWT")
async def authentication(form_data: Annotated[UserAuthSchema, Depends()]):
    login_data = await controller.create_user(form_data)
    return login_data


@router.get("/oauth2/auth", description="Authenticate by discord OAuth2")
async def discord_authentication(code: str, state: str = None):
    discord_credential = await controller.auth_discord(code)
    return discord_credential


@router.post("/login", response_model=Token, description="Login by JWT")
async def login(form_data: Annotated[LoginForm, Depends()],
                response: Response):
    login_data: Token = await controller.login_user(form_data)
    response.set_cookie(key='token', value=login_data.access_token,
                        expires=settings.access_token_expire_sec, httponly=True)
    response.headers['token'] = login_data.access_token
    return login_data


@router.get("/oauth2/login", description="Login by discord OAuth2 credentials")
async def discord_login(form_data: DiscordOAuth):
    data = await controller.login_discord(credentials=form_data)
    return data
