# Route: PATCH /api/v1/auth/rename
# Desc: 修改顯示名稱
# ------------------------------------------------------------

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select, col
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_session
from app.database.models import User
from app.schema.v1.auth.rename import Update
from app.api.v1.auth.verify_token import verify_token

router = APIRouter()

@router.patch("/rename", status_code=status.HTTP_200_OK)
async def rename(
    new_name: Update,
    user: dict = Depends(verify_token),
    db: AsyncSession = Depends(get_session)
):
    statement = select(User).where(col(User.student_id) == user["user_id"])
    result = await db.execute(statement)
    db_user = result.scalar_one_or_none()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db_user.display_name = new_name.display_name
    
    try:
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return {"state": "success"}
    except Exception as e:
        await db.rollback()
        logging.error(f"更新餐廳失敗: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="系統更新失敗"
        )
    
