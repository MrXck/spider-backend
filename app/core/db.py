from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.orm import DeclarativeBase

# MySQL + asyncmy
DATABASE_URL = "mysql+asyncmy://root:123@localhost:3306/todolist?charset=utf8mb4"

engine = create_async_engine(
    DATABASE_URL,
    pool_size=10,  # 连接池大小
    max_overflow=20,  # 超出池的最大连接数
    pool_pre_ping=True,  # 自动检测断连
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# class Base(DeclarativeBase):
#     pass


# FastAPI 依赖
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
