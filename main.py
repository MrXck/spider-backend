from fastapi import FastAPI

from app.api import user
from app.common.R import R

app = FastAPI()
app.include_router(
    user.router,
    prefix="/user",
    tags=["user"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}}
)


@app.get("/")
def root():
    return R.success({"msg": "FastAPI running on Windows!"})
