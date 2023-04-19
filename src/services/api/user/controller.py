from pydantic import EmailStr

from src.repository.repository import Repository
from src.services.api.user.schema import UserInDB, UserSchema


class UserController:

    def __init__(self, db: Repository):
        self.db = db

    async def update_user(self, user_in_db: UserInDB) -> UserSchema:
        return await self.db.create_user(user_in_db)

    async def get_user_by_email(self, email: EmailStr) -> UserInDB:
        return await self.db.get_user_by_field(field="email", value=email)
