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

router = APIRouter()

@router.get("/{store_id}/orders", response_model=List[StoreOrders])
async def get_store_orders(store_id: UUID, db: AsyncSession = Depends(get_session)):
    statement = select(Order).where(col(Order.store_id) == store_id)
    select_result = await db.execute(statement)
    orders = select_result.scalars().all()
    logging.debug(f"已取得{store_id}的訂單資料")
    return orders