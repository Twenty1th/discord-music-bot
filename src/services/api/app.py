from fastapi import FastAPI

from src.services.api.auth.router import router as auth_router
from src.services.api.user.router import router as user_router

__all__ = ['api']

api = FastAPI()
api.include_router(prefix="/api/v1/auth", router=auth_router)
api.include_router(prefix="/api/v1/profile", router=user_router)
