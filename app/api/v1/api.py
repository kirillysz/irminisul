from fastapi import FastAPI
from .routers import data, routes

root = FastAPI()

root.include_router(
    data.router
)

root.include_router(
    routes.router
)
