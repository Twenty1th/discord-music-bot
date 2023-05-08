import uvicorn
from fastapi import FastAPI

from api_v1.auth.router import router as auth_router
from api_v1.user.router import router as user_router

__all__ = ['app']

from core.settings import get_settings

settings = get_settings()

app = FastAPI()
app.include_router(router=auth_router, prefix='/api_v1')
app.include_router(router=user_router, prefix='/api_v1')

if __name__ == '__main__':
    uvicorn.run(app, port=settings.api_port, workers=settings.workers)
