from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api import user
from app.core.security import RequireLogin

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
