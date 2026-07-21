from typing import Optional

from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


class UserCreate(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=1, max_length=50)
    email: Optional[EmailStr] = Field(default=None, max_length=250)
    enable_email: Optional[bool] = Field(default=False, alias='enableEmail')
    ios_path: Optional[str] = Field(default=None, max_length=250, alias='iosPath')
    enable_ios: Optional[bool] = Field(default=False, alias='enableIos')
    android_path: Optional[str] = Field(default=None, max_length=250, alias='androidPath')
    enable_android: Optional[bool] = Field(default=False, alias='enableAndroid')


class UserLogin(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=1, max_length=50)


class UserBase(BaseModel):
    id: int
    username: str
    email: Optional[EmailStr]
    enable_email: bool
    ios_path: str
    enable_ios: bool
    android_path: str
    enable_android: bool
    create_time: datetime
    update_time: Optional[datetime]

    class Config:
        from_attributes = True


class UserRead(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    # password: str = Field(min_length=1, max_length=50)
    email: Optional[EmailStr] = Field()
    enable_email: bool = Field(default=False, alias='enableEmail')
    ios_path: str = Field(min_length=1, max_length=250, alias='iosPath')
    enable_ios: bool = Field(default=False, alias='enableIos')
    android_path: str = Field(min_length=1, max_length=250, alias='androidPath')
    enable_android: bool = Field(default=False, alias='enableAndroid')
    create_time: datetime = Field(alias='createTime')
    update_time: Optional[datetime] = Field(default=None, alias='updateTime')

    class Config:
        from_attributes = True  # 允许从 ORM 对象读属性
        populate_by_name = True  # 允许通过原名或别名都能传值
