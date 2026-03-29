# Route: GET /api/v1/auth/verify
# Desc: 驗證使用者Token(JWT)
# ------------------------------------------------------------

from fastapi import APIRouter, Depends
from app.schema.v1.auth.verify_token import VerifyToken
from app.core.jwt_manager import decode_jwt

router = APIRouter()


@router.get("/verify", response_model=VerifyToken)
async def verify_token(account: dict = Depends(decode_jwt)):
    return {
        "user_id": account["user_id"],
        "display_name": account["display_name"],
        "role": account["role"],
        "status": "active"
    }





