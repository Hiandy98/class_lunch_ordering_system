# Route: GET /api/v1/store/today
# Desc: 取得今日店家列表
# ------------------------------------------------------------

import logging
from fastapi import APIRouter, Depends
from sqlmodel import select, col
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_session
from app.database.models import Store
from app.schema.v1.stores.list import AllStore

router = APIRouter()

@router.get("/list/today", response_model=list[AllStore])
async def get_today_store(db: AsyncSession = Depends(get_session)):
    statement = select(Store).where(col(Store.is_today_store) == True)
    select_result = await db.execute(statement)
    stores = select_result.scalars().all()
    logging.info(f"已取得所有商店，共{len(stores)}筆資料")
    return stores