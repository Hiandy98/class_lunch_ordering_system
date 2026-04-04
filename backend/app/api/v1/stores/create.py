# Route: POST /api/v1/store/create
# Desc: 建立新菜單
# ------------------------------------------------------------

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_session
from app.database.models import Store
from app.schema.v1.stores.create import Create, StoreCreate

router = APIRouter()

@router.post("/create", response_model=Create, status_code=status.HTTP_201_CREATED)
async def create_store(payload: StoreCreate,
                        db: AsyncSession = Depends(get_session)):
    logging.debug("新增餐廳操作")
    new_store = Store(
        name=payload.name,
        menu_url=payload.menu_url
    )

    try:
        db.add(new_store)
        await db.commit()
        await db.refresh(new_store)
        return new_store
    except Exception as e:
        await db.rollback()
        logging.error(f"資料庫寫入失敗: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="系統寫入資料庫時發生未知錯誤"
        )