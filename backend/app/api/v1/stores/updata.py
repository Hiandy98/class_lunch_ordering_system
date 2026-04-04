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
from datetime import datetime


router = APIRouter()

@router.patch("/{store_id}/updata/active")
async def patch_active_status(store_id: UUID, is_active: bool, db: AsyncSession = Depends(get_session)):
    statement = select(Store).where(col(Store.id) == store_id)
    result = await db.execute(statement)
    target_store = result.scalar_one_or_none()
    
    if not target_store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not Found"
        )
    
    target_store.sqlmodel_update({"is_active": is_active})
    
    try:
        db.add(target_store)
        await db.commit()
        await db.refresh(target_store)
    except Exception as e:
        await db.rollback()
        logging.error(f"資料庫寫入失敗: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="系統寫入資料庫時發生未知錯誤"
        )
    return {
        "state": "success"
    }


@router.patch("/{store_id}/updata/deadline")
async def set_deadline(store_id: UUID, deadline: datetime, db: AsyncSession = Depends(get_session)):
    statement = select(Store).where(col(Store.id) == store_id)
    result = await db.execute(statement)
    target_store = result.scalar_one_or_none()
    
    if not target_store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not Found"
        )
    
    target_store.sqlmodel_update({"deadline": deadline})
    
    try:
        db.add(target_store)
        await db.commit()
        await db.refresh(target_store)
    except Exception as e:
        await db.rollback()
        logging.error(f"資料庫寫入失敗: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="系統寫入資料庫時發生未知錯誤"
        )
    return {
        "state": "success"
    }
    

@router.patch("/{store_id}/updata/today")
async def set_today(store_id: UUID, is_today: bool, db: AsyncSession = Depends(get_session)):
    statement = select(Store).where(col(Store.id) == store_id)
    result = await db.execute(statement)
    target_store = result.scalar_one_or_none()
    
    if not target_store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not Found"
        )
    
    target_store.sqlmodel_update({"is_today_store": is_today})
    
    try:
        db.add(target_store)
        await db.commit()
        await db.refresh(target_store)
    except Exception as e:
        await db.rollback()
        logging.error(f"資料庫寫入失敗: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="系統寫入資料庫時發生未知錯誤"
        )
    return {
        "state": "success"
    }
    
@router.patch("/{store_id}/updata/name")
async def change_name(store_id: UUID, name: str, db: AsyncSession = Depends(get_session)):
    statement = select(Store).where(col(Store.id) == store_id)
    result = await db.execute(statement)
    target_store = result.scalar_one_or_none()
    
    if not target_store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not Found"
        )
    
    target_store.sqlmodel_update({"name": name})
    
    try:
        db.add(target_store)
        await db.commit()
        await db.refresh(target_store)
    except Exception as e:
        await db.rollback()
        logging.error(f"資料庫寫入失敗: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="系統寫入資料庫時發生未知錯誤"
        )
    return {
        "state": "success"
    }
    
