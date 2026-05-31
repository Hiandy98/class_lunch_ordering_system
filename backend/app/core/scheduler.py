import logging
import httpx
from datetime import datetime, time
from pytz import timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.core.lock_service import lock_expired_stores_and_orders

tz_taiwan = timezone('Asia/Taipei')
scheduler = AsyncIOScheduler(timezone=tz_taiwan)

async def keep_backend_awake():
    """定時自我喚醒(每日 07:30 ~ 14:00 台灣時間)"""
    now_taiwan = datetime.now(tz_taiwan)
    current_time = now_taiwan.time()
    
    start_awake = time(7, 30, 0)
    end_awake = time(14, 0, 0)
    
    if not (start_awake <= current_time <= end_awake):
        logging.info(f"[Scheduler] Current Taiwan time {current_time.strftime('%H:%M')} is in sleeping hours. Skip ping.")
        return

    url = "https://class-lunch-ordering-system.onrender.com"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10.0)
            if response.status_code == 200:
                logging.info(f"[Scheduler] Taiwan time {now_taiwan.strftime('%H:%M')} self-ping success. Server stays alive.")
            else:
                logging.warning(f"[Scheduler] Self-ping returned abnormal status: {response.status_code}")
    except Exception as e:
        logging.error(f"[Scheduler] Self-ping connection failed: {e}")

def start_scheduler():
    current_time_with_tz = datetime.now(tz_taiwan)
    
    scheduler.add_job(
        lock_expired_stores_and_orders,
        trigger=IntervalTrigger(minutes=1),
        id="lock_expired_stores",
        replace_existing=True,
        next_run_time=current_time_with_tz
    )
    
    scheduler.add_job(
        keep_backend_awake,
        trigger=IntervalTrigger(minutes=10),
        id="keep_awake_job",
        replace_existing=True,
        next_run_time=current_time_with_tz
    )
    
    scheduler.start()
    print("定時任務調度器已啟動 - 餐廳鎖定與時區安全自我喚醒功能已就緒")

def shutdown_scheduler():
    scheduler.shutdown()
    print("定時任務調度器已關閉")
