from fastapi import APIRouter
from app.api.v1.orders.list import router as order_list_router
from app.api.v1.orders.today import router as today_router
from app.api.v1.orders.create import router as create_router
from app.api.v1.orders.cancel import router as cancel_router

order_router = APIRouter()

order_router.include_router(order_list_router)
order_router.include_router(today_router)
order_router.include_router(create_router)
order_router.include_router(cancel_router)