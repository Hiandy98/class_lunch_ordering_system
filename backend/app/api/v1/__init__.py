from fastapi import APIRouter
from app.api.v1.stores import store_router

api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(store_router, prefix="/store", tags=["Stores"])