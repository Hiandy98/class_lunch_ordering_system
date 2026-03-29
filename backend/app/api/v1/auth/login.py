import logging
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlmodel import select, col
from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models.user import User
from app.database.session import get_session
from app.core.password import safe_verify_password
from app.core.jwt_manager import create_access_token, REMEMBER_ME_EXPIRE_DAYS
from app.schema.v1.auth.login import Login


router = APIRouter()

async def account_verify(user: str ,password: str,
                         db: AsyncSession = Depends(get_session)) -> User:
    logging.debug("正在嘗試取得資料")
    statement = select(User).where(or_(
        col(User.student_id) == user,
        col(User.display_name) == user))
    
    select_results = await db.execute(statement)
    user_info = select_results.scalars().first()
    if not user_info:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="未知的使用者名稱或ID"
            )
    
    user_id = user_info.student_id
    user_hash_password = user_info.hashed_password
    pwd_verity_state = await safe_verify_password(user_id, user_hash_password, password)
    if not pwd_verity_state:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="使用者密碼輸入錯誤"
            )
    
    return user_info
    

@router.post("/login", response_model=Login)
async def login(response: Response, remember_me: bool = False, user_account: User = Depends(account_verify)):
    user_id = user_account.student_id
    username = user_account.display_name
    expire = timedelta(days=REMEMBER_ME_EXPIRE_DAYS)
    token = create_access_token(user_id, username, expire)

    cookies_age = REMEMBER_ME_EXPIRE_DAYS * 86400 if remember_me else None
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=cookies_age,
        samesite="lax",
        secure=True
    )

    return {
        "state": "登入成功"
    }

