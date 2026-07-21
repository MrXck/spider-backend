import datetime

from sqlalchemy import Column, String, BigInteger, SmallInteger, DateTime

from app.models.base import Base


class User(Base):
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    enable_email = Column(SmallInteger(), default=0, nullable=False)
    email = Column(String(255), nullable=True)
    enable_ios = Column(SmallInteger(), default=0, nullable=False)
    ios_path = Column(String(255), nullable=True)
    enable_android = Column(SmallInteger(), default=0, nullable=False)
    android_path = Column(String(255), nullable=True)
    create_time = Column(DateTime(), default=datetime.datetime.now(), nullable=False)
    update_time = Column(DateTime(), nullable=True)
