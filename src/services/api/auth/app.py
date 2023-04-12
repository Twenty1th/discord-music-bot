from fastapi import FastAPI

from .view import router

app = FastAPI()
app.include_router(router)
