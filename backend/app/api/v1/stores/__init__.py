from fastapi import APIRouter
from api.v1.stores.list import router as store_list_router

store_router = APIRouter()

store_router.include_router(store_list_router)