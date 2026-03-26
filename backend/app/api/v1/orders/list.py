# Route: GET /api/v1/orders/list
# Desc: 取得所有存取訂單的資料
# ------------------------------------------------------------

import logging
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_session
from app.database.models.order import Order
from app.schema.v1.orders.list import AllOrder

router = APIRouter()

@router.get("/list", response_model=list[AllOrder])
async def get_all_order(db: AsyncSession = Depends(get_session)):
    logging.debug("正在嘗試取得資料")
    statement = select(Order)
    select_results = await db.execute(statement)
    orders = select_results.all()
    logging.info(f"已取得所有商店，共{len(orders)}筆資料")
    return orders

