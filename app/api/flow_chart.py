from fastapi import APIRouter, Depends
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.R import R
from app.core.db import get_db
from app.core.security import RequireLogin, get_current_user
from app.models.flow_chart import FlowChart
from app.schemas.flow_chart import FlowChartCreate, FlowChartUpdate, FlowChartPage, FlowChartRead
from app.utils.constant import FLOW_CHART_NOT_EXISTS_ERROR, FLOW_CHART_ALREADY_EXIST_ERROR
from app.utils.page_utils import get_page_info

router = APIRouter()


@router.get(
    "/{flow_id}",
    dependencies=[RequireLogin],
)
async def get_by_flow_id(
        flow_id: int,
        user_info: dict = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    flow_chart = (
        await db.execute(
            select(FlowChart).where(FlowChart.id == flow_id, FlowChart.user_id == user_info.get('user_id')))
    ).scalars().first()
    if flow_chart is None:
        return R.error(FLOW_CHART_NOT_EXISTS_ERROR)
    flow_chart = FlowChartRead.model_validate(flow_chart).model_dump(by_alias=True)
    return R.success({"flowChart": flow_chart})


@router.post(
    "/add",
    dependencies=[RequireLogin]
)
async def add_flow(flow_chart: FlowChartCreate,
                   user_info: dict = Depends(get_current_user),
                   db: AsyncSession = Depends(get_db)):
    already_flow_chart = (
        await db.execute(select(FlowChart).where(FlowChart.name == flow_chart.name))
    ).scalars().first()
    if already_flow_chart:
        return R.error(FLOW_CHART_ALREADY_EXIST_ERROR)

    db_flow_chart = FlowChart(**flow_chart.model_dump(exclude_unset=True))
    db_flow_chart.user_id = user_info.get('user_id')
    db.add(db_flow_chart)
    await db.flush()
    await db.refresh(db_flow_chart)
    return R.success({"id": db_flow_chart.id})


@router.put(
    "/",
    dependencies=[RequireLogin]
)
async def update_flow(
        new_flow_chart: FlowChartUpdate,
        user_info: dict = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        update(FlowChart)
        .where(FlowChart.id == new_flow_chart.id, FlowChart.user_id == user_info.get('user_id'))
        .values(**new_flow_chart.model_dump(exclude_unset=True))
    )

    if result.rowcount == 0:
        return R.error(FLOW_CHART_NOT_EXISTS_ERROR)

    return R.success({"id": new_flow_chart.id})


@router.delete(
    "/{flow_id}",
    dependencies=[RequireLogin],
)
async def delete_by_flow_id(
        flow_id: int,
        user_info: dict = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        delete(FlowChart)
        .where(
            FlowChart.id == flow_id,
            FlowChart.user_id == user_info.get('user_id')
        )
        .execution_options(synchronize_session="fetch")
    )
    await db.commit()

    if result.rowcount == 0:
        return R.error(FLOW_CHART_NOT_EXISTS_ERROR)

    return R.success({"deleted_id": flow_id})


@router.post(
    "/page",
    dependencies=[RequireLogin]
)
async def get_by_page(
        flow_chart: FlowChartPage,
        user_info: dict = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    size = flow_chart.page_size
    page = flow_chart.page_num

    where = (
        select(FlowChart)
        .where(
            FlowChart.user_id == user_info.get('user_id'),
            FlowChart.name.like(f"%{flow_chart.name}%")
        )
    )

    return R.success(await get_page_info(where, page, size, db, FlowChartRead))
