import os
import httpx
import logging
from dotenv import load_dotenv

load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

async def send_discord_notification(store_name: str, store_id: str, locked_orders_count: int):
    if not DISCORD_WEBHOOK_URL:
        logging.warning("未設置 DISCORD_WEBHOOK_URL, 跳過通知發送")
        return

    content = (
        f"🔒 **餐廳截單通知**\n"
        f"餐廳：{store_name}\n"
        f"ID:`{store_id}`\n"
        f"狀態：已過截單時間，餐廳已關閉接單入口\n"
        f"鎖定訂單數：{locked_orders_count} 笔\n"
        f"時間：<t:{int(__import__('time').time())}:F>"
    )

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                DISCORD_WEBHOOK_URL,
                json={"content": content},
                timeout=10.0
            )
            response.raise_for_status()
            logging.info(f"已發送 Discord 通知：{store_name}")
    except Exception as e:
        logging.error(f"發送 Discord 通知失敗: {e}")