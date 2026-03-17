# Route: GET /api/v1/store/list
# Desc: 取得所有合作商店清單
# ------------------------------------------------------------

import logging
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.database.session import get_session
from app.database.models import Store
from app.schema.v1.stores.list import AllStore

router = APIRouter()

@router.get("/list", response_model=list[AllStore])
def get_all_store(db: Session = Depends(get_session)):
    statement = select(Store)
    stores = db.exec(statement).all()
    logging.info(f"已取得所有商店，共{len(stores)}筆資料")
    return stores