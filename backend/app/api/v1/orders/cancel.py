# Route: POST /api/v1/order/cancel
# Desc: 取消訂單
# ------------------------------------------------------------

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select, col
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_session
from app.database.models import Order
from app.api.v1.auth.verify_token import verify_token
from uuid import UUID

router = APIRouter()

@router.patch("/cancel")
async def cancel_order(id: UUID, account = Depends(verify_token),
                        db: AsyncSession = Depends(get_session)):
    statement = select(Order).where(col(Order.id) == id)
    result = await db.execute(statement)
    target_order = result.scalar_one_or_none()

    if not target_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not Found"
        )
    
    if account["user_id"] != target_order.student_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="你沒有權限取消此訂單"
        )

    target_order.is_active = False
    
    try:
        db.add(target_order)
        await db.commit()
        await db.refresh(target_order)
        return target_order
    except Exception as e:
        await db.rollback()
        logging.error(f"資料庫寫入失敗: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="系統寫入資料庫時發生未知錯誤"
        )