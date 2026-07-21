from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.R import R
from app.core.db import get_db
from app.core.security import RequireLogin, get_current_user
from app.models.user import User
from app.schemas.user import UserRead, UserCreate, UserLogin
from app.utils import md5
from app.utils.constant import USERNAME_OR_PASSWORD_ERROR, USERNAME_ALREADY_EXIST
from app.utils.jwt_utils import create_token

router = APIRouter()


@router.post("/login")
async def login(
        user: UserLogin,
        db: AsyncSession = Depends(get_db),
):
    login_user = (await db.execute(
        select(User).where(User.username == user.username,
                           User.password == md5.md5hex(user.password)))).scalars().first()
    if login_user:
        return R.success({
            'user': UserRead.model_validate(login_user).model_dump(),
            'token': create_token(login_user.id)
        })
    return R.error(USERNAME_OR_PASSWORD_ERROR)


@router.get("/{user_id}", dependencies=[RequireLogin],)
async def get_by_user_id(user_id: int, user_info: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    print(user_info)
    if user is None:
        return R.error(USERNAME_OR_PASSWORD_ERROR)
    user_read = UserRead.model_validate(user)
    return R.success({"user": user_read})


@router.post("/register")
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    already_user = (
        await db.execute(select(User).where(User.username == user.username))
    ).scalars().first()
    if already_user:
        return R.error(USERNAME_ALREADY_EXIST)

    db_user = User(**user.model_dump(exclude_unset=True))
    db_user.password = md5.md5hex(db_user.password)
    db.add(db_user)
    await db.flush()
    await db.refresh(db_user)
    return R.success({"id": db_user.id})
