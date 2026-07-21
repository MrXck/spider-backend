from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.R import R
from app.core.db import get_db
import app.models.user

fast = FastAPI()


@fast.get("/")
def root():
    return R.success({"msg": "FastAPI running on Windows!"})


@fast.post("/test/")
async def create_workflow(
        db: AsyncSession = Depends(get_db),
):
    wf = app.models.user.User(username='666')
    db.add(wf)
    await db.flush()
    await db.refresh(wf)
    return R.success({"id": wf.id})
