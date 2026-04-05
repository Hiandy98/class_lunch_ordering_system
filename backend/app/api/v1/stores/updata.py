# Route: GET /api/v1/store/{store_id}/update
# Desc: 修改目標餐廳之數據
# ------------------------------------------------------------

import logging
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select, col
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_session
from app.database.models import Store
from datetime import timezone
from app.schema.v1.stores.update import Update

router = APIRouter()


@router.patch("/{store_id}/update", status_code=status.HTTP_200_OK)
async def update_store_data(
    store_id: UUID,
    payload: Update,
    db: AsyncSession = Depends(get_session)
):
    statement = select(Store).where(col(Store.id) == store_id)
    result = await db.execute(statement)
    target_store = result.scalar_one_or_none()
    
    if not target_store:
        raise HTTPException(status_code=404, detail="找不到該餐廳")
    
    update_data = payload.model_dump(exclude_unset=True)
    
    if "deadline" in update_data and update_data["deadline"] is not None:
        update_data["deadline"] = update_data["deadline"].astimezone(timezone.utc).replace(tzinfo=None)

    target_store.sqlmodel_update(update_data)
    
    try:
        db.add(target_store)
        await db.commit()
        await db.refresh(target_store)
        return {"state": "success", "data": target_store}
    except Exception as e:
        await db.rollback()
        logging.error(f"更新餐廳失敗: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="系統更新失敗"
        )
