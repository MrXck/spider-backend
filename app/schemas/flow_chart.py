from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, EmailStr, ConfigDict


class FlowChartCreate(BaseModel):
    name: str = Field(min_length=1, nullable=False)
    flow_json: str = Field(min_length=1, nullable=False)


class FlowChartUpdate(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(min_length=1, nullable=False)
    flow_json: str = Field(min_length=1, nullable=False)


class FlowChartPage(BaseModel):
    name: str = Field(min_length=0, nullable=True)
    page_size: int = Field(gt=0, alias='pageSize')
    page_num: int = Field(gt=0, alias='pageNum')


class FlowChartRead(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )

    id: int = Field()
    name: str = Field()
    flow_json: str = Field(alias='flowJson')
    create_time: datetime = Field(alias='createTime')
    update_time: Optional[datetime] = Field(default=None, alias='updateTime')

