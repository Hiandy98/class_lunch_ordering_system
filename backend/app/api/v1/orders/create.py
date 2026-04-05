# Route: POST /api/v1/order/create
# Desc: 送出訂單
# ------------------------------------------------------------

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_session
from app.database.models import Order
from app.schema.v1.orders.create import OrderCreate
from app.api.v1.auth.verify_token import verify_token

router = APIRouter()

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_order(payload: OrderCreate, account = Depends(verify_token),
                        db: AsyncSession = Depends(get_session)):
    logging.debug("新增餐廳操作")
    order_items_list = [item.model_dump() for item in payload.content]
    new_order = Order(
        student_id=account["user_id"],
        store_id=payload.store_id,
        content=order_items_list,
        total_price=payload.total_price,
        is_active=True,
    )
    try:
        db.add(new_order)
        await db.commit()
        await db.refresh(new_order)
        return new_order
    except Exception as e:
        await db.rollback()
        logging.error(f"資料庫寫入失敗: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="系統寫入資料庫時發生未知錯誤"
        )