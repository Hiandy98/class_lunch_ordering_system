# Route: GET /api/v1/store/{store_id}/orders
# Desc: 取得目標餐廳之所有訂單
# ------------------------------------------------------------

import logging
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlmodel import select, col
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_session
from app.database.models import Order
from app.schema.v1.stores.orders import StoreOrders
from datetime import datetime, time, timedelta, timezone

TW_TZ = timezone(timedelta(hours=8))
router = APIRouter()

@router.get("/{store_id}/orders", response_model=List[StoreOrders])
async def get_store_orders(store_id: UUID, db: AsyncSession = Depends(get_session)):
    now_tw = datetime.now(TW_TZ)
    tw_start = datetime.combine(now_tw.date(), time.min).replace(tzinfo=TW_TZ)
    tw_end = tw_start + timedelta(days=1)

    utc_start_naive = tw_start.astimezone(timezone.utc).replace(tzinfo=None)
    utc_end_naive = tw_end.astimezone(timezone.utc).replace(tzinfo=None)

    statement = select(Order).where(
        col(Order.created_at) >= utc_start_naive,
        col(Order.created_at) < utc_end_naive,
        col(Order.store_id) == store_id,
    )
    select_result = await db.execute(statement)
    orders = select_result.scalars().all()
    logging.debug(f"已取得{store_id}的訂單資料")
    return orders