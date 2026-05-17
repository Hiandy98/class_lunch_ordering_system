# Route: POST /api/v1/stores/{store_id}/upload-menu
# Desc: 上傳多張菜單圖片至 ImgBB 並更新至店家的 menu_url ARRAY
# ------------------------------------------------------------

import logging
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlmodel import select
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.attributes import flag_modified
from app.database.session import get_session
from app.database.models.store import Store
from app.core.url_changer import upload_to_imgbb
from typing import Annotated
from pydantic import WithJsonSchema

router = APIRouter()

# 比免Swagger UI 無法上船異常... 先暴力解決
SwaggerFile = Annotated[UploadFile, WithJsonSchema({"type": "string", "format": "binary"})]

@router.post("/stores/{store_id}/upload-menu", status_code=status.HTTP_200_OK, response_model=list[str])
async def upload_store_menu(
    store_id: UUID,
    files: list[SwaggerFile] = File(...),
    db: AsyncSession = Depends(get_session)
):
    statement = select(Store).where(Store.id == store_id)
    select_results = await db.execute(statement)
    store = select_results.scalar()

    if not store:
        raise HTTPException(status_code=404, detail="找不到該店家")

    new_urls = []
    for file in files:
        if not file.content_type or not file.content_type.startswith("image/"):
            logging.warning(f"跳過非圖片檔案: {file.filename}")
            continue
                
        uploaded_url = await upload_to_imgbb(file)
        if uploaded_url:
            new_urls.append(uploaded_url)

    if not new_urls:
        raise HTTPException(status_code=400, detail="所有圖片上傳皆失敗或未提供有效圖片")

    current_menu = store.menu_url if store.menu_url is not None else []
    store.menu_url = current_menu + new_urls
    
    flag_modified(store, "menu_url")

    try:
        db.add(store)
        await db.commit()
        await db.refresh(store)
    except Exception as e:
        await db.rollback()
        logging.error(f"資料庫更新失敗: {e}")
        raise HTTPException(status_code=500, detail="資料庫寫入失敗")

    return store.menu_url
