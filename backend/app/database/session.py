import os
import sys
import logging
import socket
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from sqlalchemy.exc import OperationalError, ProgrammingError
from dotenv import load_dotenv

load_dotenv()

# 檢查環境變數
database_url = os.getenv("DATABASE_URL")
if not database_url:
    logging.critical("環境變數 DATABASE_URL 缺失！")
    sys.exit(1)

# 非同步 Engine
engine = create_async_engine(
    database_url,
    echo=True,
    pool_pre_ping=True,     # 防止 Supabase 自動斷線
    pool_recycle=1800,      # 每 30 分鐘重置連線
    pool_size=5,
    max_overflow=0,          # 不讓連線數超出預期
    connect_args={
        "prepared_statement_cache_size": 0,
        "statement_cache_size": 0  # 雙重保險，確保 asyncpg 徹底關閉快取
    }
)

# 非同步 Session 工廠
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False
)
# 非同步連線測試
async def connect_check():
    """
    在 main.py 啟動時呼叫： await connect_check()
    """
    try:
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT 1"))
            # 確保資料確實讀取完畢
            result.scalar()
            logging.info("Supabase 非同步資料庫連線測試成功")
    except OperationalError as e:
        underlying_err = getattr(e, "orig", None)
        
        if underlying_err:
            err_msg = str(underlying_err).lower()
            
            if isinstance(underlying_err, socket.gaierror) or "getaddrinfo failed" in err_msg:
                logging.critical("Supabase錯誤: 找不到資料庫主機 請檢查 Supabase 後台專案是否被 暫停 或 URL 填寫錯誤")
                sys.exit(1)

            if isinstance(underlying_err, (OSError, socket.error, TimeoutError)) or "connection refused" in err_msg or "timed out" in err_msg:
                logging.critical("Supabase錯誤: 連線被拒絕或超時 資料庫伺服器可能未開啟 正在重啟中 或專案已被暫停")
                sys.exit(1)
                
        logging.critical(f"無法連線（網路、密碼或連線數已滿）: {e}")
        sys.exit(1)
    except ProgrammingError as e:
        logging.critical(f"權限、資料庫名稱或語法錯誤: {e}")
        sys.exit(1)
    except Exception as e:
        logging.critical(f"發生未預期的錯誤: {e}")
        sys.exit(1)

# 非同步取得 Session 方法
async def get_session():
    """
    FastAPI 注入建議： async with AsyncSessionLocal() as session:
    """
    async with AsyncSessionLocal() as session:
        yield session
