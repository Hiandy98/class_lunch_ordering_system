from fastapi import APIRouter
from app.api.v1.stores.list import router as store_list_router
from app.api.v1.stores.today import router as today_store_router
from app.api.v1.stores.menu import router as menu_router
from app.api.v1.stores.create import router as create_router

store_router = APIRouter()

store_router.include_router(store_list_router)
store_router.include_router(today_store_router)
store_router.include_router(menu_router)
store_router.include_router(create_router)