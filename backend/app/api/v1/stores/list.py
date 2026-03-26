# Route: GET /api/v1/store/list
# Desc: 取得所有合作商店清單
# ------------------------------------------------------------

import logging
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_session
from app.database.models import Store
from app.schema.v1.stores.list import AllStore

router = APIRouter()

@router.get("/list", response_model=list[AllStore])
async def get_all_store(db: AsyncSession = Depends(get_session)):
    statement = select(Store)
    select_result = await db.execute(statement)
    stores = select_result.all()
    logging.info(f"已取得所有商店，共{len(stores)}筆資料")
    return stores