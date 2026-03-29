from fastapi import APIRouter
from app.api.v1.auth.login import router as login_router

auth_router = APIRouter()

auth_router.include_router(login_router)