from uuid import UUID

from src.repository.repository import Repository
from src.services.api.user.schema import UserUpdateSchema, UserInDB


class TestDB(Repository):
    fake_users_db = {
        "johndoe": {
            "username": "johndoe",
            "full_name": "John Doe",
            "email": "johndoe@example.com",
            "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
            "discord_id": 0,
            "discord_servers": []
        }
    }

    def get_user(self, uuid: UUID):
        pass

    def create_user(self, user: UserInDB):
        pass

    def update_user(self, new_user: UserUpdateSchema):
        pass

    def delete_user(self, uuid: UUID):
        pass
