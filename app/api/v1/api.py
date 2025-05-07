from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import data, routes

root = FastAPI()
root.add_middleware(
    CORSMiddleware,
    allow_origins=["https://irminsul.space"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



root.include_router(
    data.router
)

root.include_router(
    routes.router
)
