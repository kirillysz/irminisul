from fastapi import FastAPI
from .routers import data

root = FastAPI()

root.include_router(
    data.router
)
