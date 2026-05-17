import httpx
import os
import logging
import sys
from dotenv import load_dotenv
from fastapi import UploadFile
from typing import Optional

load_dotenv()
IMGBB_KEY = os.getenv("IMGBB_KEY")
if not IMGBB_KEY:
    logging.critical("IMGBB_KEY缺失")
    sys.exit(1)

async def upload_to_imgbb(file: UploadFile) -> Optional[str]:
    async with httpx.AsyncClient() as client:
        try:
            await file.seek(0)
            file_content = await file.read()
            
            if not file_content:
                logging.error(f"檔案內容為空: {file.filename}")
                return None

            content_type = file.content_type or "image/jpeg"
            files_payload = {
                "image": (file.filename, file_content, content_type)
            }
            
            url = "https://api.imgbb.com/1/upload"
            params_payload = {"key": IMGBB_KEY}
            
            response = await client.post(
                url, 
                params=params_payload, 
                files=files_payload,
                timeout=20.0
            )
            
            if "application/json" in response.headers.get("content-type", ""):
                result = response.json()
                if response.status_code == 200 and result.get("success") is True:
                    return result["data"]["url"]
                else:
                    logging.error(f"ImgBB 拒絕上傳，結構為: {result}")
                    return None
            else:
                logging.critical(f"ImgBB 回傳狀態碼: {response.status_code}, 內容: {response.text[:200]}")
                return None

        except Exception as e:
            logging.error(f"網路連線或上傳發生例外狀況: {e}")
            return None
        finally:
            await file.seek(0)
