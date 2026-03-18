from fastapi import APIRouter
from app.api.v1.orders.list import router as order_list_router

order_router = APIRouter()

order_router.include_router(order_list_router)