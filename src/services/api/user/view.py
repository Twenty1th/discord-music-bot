from fastapi import APIRouter

from src.services.api.auth.heplers import get_current_user
from src.services.api.user.schema import User

router = APIRouter(
    prefix="/my-profile"
)


@router.post("", response_model=User)
async def get_owner_profile(token: str | None):
    return await get_current_user(token)
