# Route: POST /api/v1/order/create
# Desc: 送出訂單
# ------------------------------------------------------------

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, col
from app.database.session import get_session
from app.database.models import Order, Store
from app.schema.v1.orders.create import OrderCreate
from app.api.v1.auth.verify_token import verify_token

router = APIRouter()

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_order(payload: OrderCreate, account = Depends(verify_token),
                        db: AsyncSession = Depends(get_session)):
    logging.debug("新增餐點操作")

    try:
        store_stmt = select(Store).where(col(Store.id) == payload.store_id)
        store_result = await db.execute(store_stmt)
        store = store_result.scalar_one_or_none()

        if not store:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="找不到指定的餐廳"
            )
        if not store.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="該餐廳已關閉，無法下單"
            )
        if store.deadline:
            now_naive = datetime.now(timezone.utc).replace(tzinfo=None)
            deadline_naive = store.deadline.replace(tzinfo=None) if store.deadline.tzinfo else store.deadline
            
            if deadline_naive <= now_naive:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="已超過該餐廳截止時間，無法下單"
                )

        order_items_list = [item.model_dump() for item in payload.content]

        new_order = Order(
            student_id=account["user_id"],
            store_id=payload.store_id,
            content=order_items_list,
            total_price=payload.total_price,
            is_active=True,
            is_locked=False
        )
    
        db.add(new_order)
        await db.commit()
        await db.refresh(new_order)
        return new_order
    
    except HTTPException:
        await db.rollback()
        raise

    except Exception as e:
        await db.rollback()
        logging.error(f"資料庫寫入失敗: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="系統寫入資料庫時發生未知錯誤"
        )