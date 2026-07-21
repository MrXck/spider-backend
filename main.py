from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api import user

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Authorization"],
)
app.include_router(
    user.router,
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}}
)
