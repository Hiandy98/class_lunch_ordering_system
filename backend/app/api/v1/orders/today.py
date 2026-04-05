# Route: GET /api/v1/orders/today
# Desc: 取得今日所有存取訂單的資料
# ------------------------------------------------------------

import logging
from fastapi import APIRouter, Depends
from sqlmodel import select, col
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_session
from app.database.models.order import Order
from app.schema.v1.orders.list import AllOrder
from datetime import datetime, time, timedelta, timezone

TW_TZ = timezone(timedelta(hours=8))
router = APIRouter()

@router.get("/today", response_model=list[AllOrder])
async def get_today_order(db: AsyncSession = Depends(get_session)):
    logging.debug("正在嘗試取得資料")
    now_tw = datetime.now(TW_TZ)
    tw_start = datetime.combine(now_tw.date(), time.min).replace(tzinfo=TW_TZ)
    tw_end = tw_start + timedelta(days=1)

    utc_start_naive = tw_start.astimezone(timezone.utc).replace(tzinfo=None)
    utc_end_naive = tw_end.astimezone(timezone.utc).replace(tzinfo=None)

    statement = select(Order).where(
        col(Order.created_at) >= utc_start_naive,
        col(Order.created_at) < utc_end_naive
    )
    select_results = await db.execute(statement)
    orders = select_results.scalars().all()
    logging.info(f"已取得所有商店，共{len(orders)}筆資料")
    return orders

