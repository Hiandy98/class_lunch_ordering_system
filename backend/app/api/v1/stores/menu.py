# Route: GET /api/v1/store/{store_id}/menu
# Desc: 取得目標餐廳之菜單
# ------------------------------------------------------------

import logging
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select, col
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_session
from app.database.models import Store
from app.schema.v1.stores.menu import Menu

router = APIRouter()

@router.get("/{store_id}/menu", response_model=Menu)
async def get_all_store(store_id: UUID, db: AsyncSession = Depends(get_session)):
    statement = select(Store.menu_url).where(col(Store.id) == store_id)
    select_result = await db.execute(statement)
    menus = select_result.scalar_one_or_none()
    if not menus:
        logging.warning(f"找不到商店 {store_id} 或該商店無菜單資料")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="無菜單資料"
        )
    logging.debug(f"已取得{store_id}的菜單資料")
    return {"menu_url": menus}