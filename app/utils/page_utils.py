import math
from typing import Type

from pydantic import BaseModel
from sqlalchemy import Select, func
from sqlalchemy.ext.asyncio import AsyncSession


async def get_page_info(where: Select, page: int, size: int, db: AsyncSession, model: Type[BaseModel]):
    stmt = (
        where
        .offset((page - 1) * size)
        .limit(size)
    )
    result = await db.execute(stmt)
    flow_chart_list = result.scalars().all()
    return_flow_chart_list = []
    for flow_chart in flow_chart_list:
        return_flow_chart_list.append(model.model_validate(flow_chart).model_dump(by_alias=True))

    count_stmt = (
        where
        .with_only_columns(func.count(), maintain_column_froms=True)
        .order_by(None)
    )
    total = await db.scalar(count_stmt)
    return {
        'records': return_flow_chart_list,
        'total': total,
        'size': size,
        'current': page,
        'pages': math.ceil(total / size)
    }
