# Route: PATCH /api/v1/auth/repwd
# Desc: 修改密碼
# ------------------------------------------------------------

import logging
import jwt
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from sqlmodel import select, col
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_session
from app.database.models.user import User
from app.schema.v1.auth.repwd import Update
from app.api.v1.auth.verify_token import verify_token
from app.core.password import safe_verify_password, safe_create_password
from app.core.jwt_manager import create_access_token, JWT_KEY, ALGORITHM 

router = APIRouter()

@router.patch("/repwd", status_code=status.HTTP_200_OK)
async def repwd(
    payload: Update,
    response: Response,
    access_token: str = Cookie(None),
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
    
    new_pwd = await safe_create_password(user_id, payload.new_pwd)
    user_info.hashed_password = new_pwd

    try:
        db.add(user_info)
        await db.commit()
        await db.refresh(user_info)

        remaining_delta = timedelta(minutes=30)
        cookies_age = None
        
        if access_token:
            try:
                old_payload = jwt.decode(access_token, JWT_KEY, algorithms=[ALGORITHM], options={"verify_exp": False})
                exp_timestamp = old_payload.get("exp")
                if exp_timestamp:
                    exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
                    now_datetime = datetime.now(timezone.utc)
                    diff = exp_datetime - now_datetime
                    
                    if diff.total_seconds() > 0:
                        remaining_delta = diff
                        if diff.total_seconds() > 86400:
                            cookies_age = int(diff.total_seconds())
            except Exception:
                pass

        new_jwt_string = create_access_token(
            user_id=user_info.student_id,
            display_name=user_info.display_name,
            role=user_info.role,
            expires_delta=remaining_delta
        )
        
        response.set_cookie(
            key="access_token",
            value=new_jwt_string,
            httponly=True,
            max_age=cookies_age,
            samesite="lax",
            secure=True
        )

        return {"state": "success"}
        
    except Exception as e:
        await db.rollback()
        logging.error(f"更新餐廳失敗: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="系統更新失敗"
        )
