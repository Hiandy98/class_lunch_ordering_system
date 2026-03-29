import os
import jwt
import sys
import logging
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from fastapi import HTTPException, status, Cookie

load_dotenv()
JWT_KEY = os.getenv("JWT_KEY")
if not JWT_KEY:
    logging.critical("JWT_KEY缺失")
    sys.exit(1)

ALGORITHM = "HS256"
DEFAULT_EXPIRE_MINUTES = 30
REMEMBER_ME_EXPIRE_DAYS = 14


def create_access_token(user_id: str, display_name: str, expires_delta: timedelta):
    payload = {
        "sub": user_id,
        "name": display_name,
        "exp": datetime.now(timezone.utc) + expires_delta
    }
    return jwt.encode(payload, JWT_KEY, algorithm=ALGORITHM)

def decode_jwt(jwt_code: str = Cookie(None)):
    if not jwt_code:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="請重新登入，目前無憑證或已過期"
        )
    try:
        payload = jwt.decode(jwt_code, JWT_KEY, algorithms=[ALGORITHM])
        
        user_id = payload.get("sub")
        display_name = payload.get("name")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="認證失敗或 Token 已過期",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return {
            "user_id": user_id,
            "display_name": display_name
        }

    except jwt.ExpiredSignatureError:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token 已過期"
            )
    except jwt.PyJWTError:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="認證失敗或 Token 已過期",
                headers={"WWW-Authenticate": "Bearer"},
            )