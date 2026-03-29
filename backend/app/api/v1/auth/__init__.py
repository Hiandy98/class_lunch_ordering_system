from fastapi import APIRouter
from app.api.v1.auth.login import router as login_router
from app.api.v1.auth.verify_token import router as verify_router
from app.api.v1.auth.logout import router as logout_router

auth_router = APIRouter()

auth_router.include_router(login_router)
auth_router.include_router(verify_router)
auth_router.include_router(logout_router)
