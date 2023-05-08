from fastapi.security import OAuth2PasswordBearer

from api_v1.schemas import User, UserInfo, UserUpdateSchema, UserID
from core.exceptions import Unauthorized, UserEmailExists
from core.security import get_user_field_from_token
from core.settings import get_settings
from repository.repository import Repository

settings = get_settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api_v1/v1/auth/login",
                                     scheme_name="JWT")


class UserController:

    def __init__(self, db: Repository):
        self.db = db

    async def update_user(self, new_user: UserUpdateSchema, token: str) -> UserInfo:
        user_old_email = get_user_field_from_token(field='sub', token=token)

        if await self.db.get_user_by_field(field='email', value=new_user.new_email):
            raise UserEmailExists
        new_params = {
            'email': new_user.new_email,
            'discord_id': new_user.new_discord_id
        }
        new_user_data = await self.db.update_user(search_field="email",
                                                  search_value=user_old_email, **new_params)
        return UserInfo(email=new_user_data.email, new_discord_id=new_user.new_discord_id)

    async def get_user(self, token: str) -> UserInfo:
        user_id: UserID = get_user_field_from_token(field="id", token=token)
        user: User = await self.db.get_user_by_field(field="id", value=user_id)
        if not user:
            raise Unauthorized

        return UserInfo(email=user.email, discord_id=user.discord_id)
