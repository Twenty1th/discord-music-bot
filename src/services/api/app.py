from fastapi import FastAPI

from src.services.api.auth.router import router as auth_router
from src.services.api.user.router import router as user_router

__all__ = ['app']

app = FastAPI()
app.include_router(auth_router)
app.include_router(user_router)
