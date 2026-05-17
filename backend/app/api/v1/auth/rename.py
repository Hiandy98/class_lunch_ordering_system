# Route: PATCH /api/v1/auth/rename
# Desc: 修改顯示名稱
# ------------------------------------------------------------

import logging
import jwt
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from sqlmodel import select, col
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_session
from app.database.models.user import User
from app.schema.v1.auth.rename import Update
from app.api.v1.auth.verify_token import verify_token
from app.core.jwt_manager import create_access_token, JWT_KEY, ALGORITHM 

router = APIRouter()

@router.patch("/rename", status_code=status.HTTP_200_OK)
async def rename(
    new_name: Update,
    response: Response,
    access_token: str = Cookie(None),
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
            user_id=db_user.student_id,
            display_name=db_user.display_name,
            role=db_user.role,
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
