import logging
from datetime import datetime, timezone
from sqlalchemy import update, func, case
from sqlmodel import select, col
from app.database.session import AsyncSessionLocal
from app.database.models.store import Store
from app.database.models.order import Order
from app.core.notify import send_discord_notification


async def lock_expired_stores_and_orders():
    """
    每分鐘執行一次：
    1. 找出所有 deadline <= now 且 is_active = True 的餐廳，並計算各自未鎖定訂單數
    2. 批次將其 is_active 設為 False (不再接受新訂單)
    3. 批次鎖定該餐廳下所有未鎖定的訂單 (is_locked = True)
    4. 安全 commit 後，再發送精準的 Discord 通知
    """
    async with AsyncSessionLocal() as db:
        expired_stores_info = []
        try:
            now = datetime.now(timezone.utc).replace(tzinfo=None)
            
            # 邏輯：如果訂單未鎖定，計為 1，否則計為 0。如果一筆訂單都沒有，coalesce 會將 NULL 轉為 0。
            stmt = (
                select(
                    Store.id, 
                    Store.name, 
                    func.coalesce(
                        func.sum(case((col(Order.is_locked) == False, 1), else_=0)), 
                        0
                    ).label("unlocked_count")
                )
                .outerjoin(Order, col(Order.store_id) == col(Store.id))
                .where(col(Store.deadline) <= now, col(Store.is_active) == True)
                .group_by(col(Store.id), col(Store.name))
            )
            
            result = await db.execute(stmt)
            expired_stores_info = result.all()  # 拿到正確的 (id, name, unlocked_count)

            if not expired_stores_info:
                logging.debug("沒有需要鎖定的餐廳")
                return

            # 收集所有需要處理的餐廳 ID
            store_ids = [store_id for store_id, _, _ in expired_stores_info]

            # 批次關閉餐廳
            await db.execute(
                update(Store)
                .where(col(Store.id).in_(store_ids))
                .values(is_active=False)
            )

            # 批次鎖定訂單
            await db.execute(
                update(Order)
                .where(col(Order.store_id).in_(store_ids), col(Order.is_locked) == False)
                .values(is_locked=True)
            )

            await db.commit()
            logging.info(f"成功批次處理 {len(store_ids)} 家過期餐廳的訂單鎖定")

        except Exception as e:
            await db.rollback()
            logging.exception(f"未知錯誤: {e}")
            return
        
        for store_id, store_name, unlocked_count in expired_stores_info:
            try:
                await send_discord_notification(
                    store_name=store_name,
                    store_id=str(store_id),
                    locked_orders_count=int(unlocked_count)
                )
                logging.info(f"餐廳 {store_id} ({store_name}) 已鎖定，關閉通知已發送")
            except Exception as notify_err:
                logging.error(f"發送餐廳 {store_id} 通知失敗: {notify_err}")

        return
