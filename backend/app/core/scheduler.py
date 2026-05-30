from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.core.lock_service import lock_expired_stores_and_orders

scheduler = AsyncIOScheduler()

def start_scheduler():
    scheduler.add_job(
        lock_expired_stores_and_orders,
        trigger=IntervalTrigger(minutes=1),
        id="lock_expired_stores",
        replace_existing=True,
        next_run_time=datetime.now()
    )
    scheduler.start()
    print("定時任務調度器已启-餐廳調度")

def shutdown_scheduler():
    scheduler.shutdown()
    print("定時任務調度器已關閉")