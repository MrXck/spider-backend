from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api import user
from app.api import flow_chart

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
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
app.include_router(
    flow_chart.router,
    prefix="/flow",
    tags=["flow"],
    responses={404: {"description": "Not found"}}
)
