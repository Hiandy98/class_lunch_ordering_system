# Route: PATCH /api/v1/auth/repwd
# Desc: 修改密碼
# ------------------------------------------------------------

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select, col
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_session
from app.database.models import User
from app.schema.v1.auth.repwd import Update
from app.api.v1.auth.verify_token import verify_token
from app.core.password import safe_verify_password, safe_create_password

router = APIRouter()

router.patch("/update", status_code=status.HTTP_200_OK)
async def repwd(
    payload: Update,
    user: dict = Depends(verify_token),
    db: AsyncSession = Depends(get_session)
):
    statement = select(User).where(col(User.student_id) == user["user_id"])
    result = await db.execute(statement)
    user_info = result.scalar_one_or_none()
    if not user_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    user_id = user_info.student_id
    user_hash_password = user_info.hashed_password
    pwd_verity_state = await safe_verify_password(user_id, user_hash_password, payload.old_pwd)
    if not pwd_verity_state:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="使用者密碼輸入錯誤"
            )
    new_pwd = safe_create_password(user_id, payload.new_pwd)
    user_info.hashed_password = str(new_pwd)

    try:
        db.add(user_info)
        await db.commit()
        await db.refresh(user_info)
        return {"state": "success", "data": user_info}
    except Exception as e:
        await db.rollback()
        logging.error(f"更新餐廳失敗: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="系統更新失敗"
        )
    
