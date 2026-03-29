from fastapi import APIRouter
from app.api.v1.stores import store_router
from app.api.v1.orders import order_router
from app.api.v1.auth import auth_router

api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(store_router, prefix="/store", tags=["Stores"])
api_v1_router.include_router(order_router, prefix="/order", tags=["Orders"])
api_v1_router.include_router(auth_router, prefix="/auth", tags=["Auth"])