import os
import sys
import logging
from sqlmodel import create_engine, Session
from sqlalchemy.exc import ArgumentError, OperationalError, ProgrammingError
from dotenv import load_dotenv

load_dotenv()

# 靜態檢查連線池的建立
database_url = os.getenv("DATABASE_URL")
if not database_url:
    logging.critical("環境變數 DATABASE_URL 缺失！")
    sys.exit(1)

try:
    engine = create_engine(database_url, echo=True)
except ArgumentError as e:
    logging.critical(f"資料庫 URL 格式錯誤: {e}")
    sys.exit(1)

# 連線測試方法
def connect_check():
    """
    這是一個主動檢查函式。
    建議只在 main.py 啟動時呼叫一次，而不是放在模組最外層。
    """
    try:
        with engine.connect():
            logging.info("資料庫連線測試成功！")
    except OperationalError as e:
        logging.critical(f"無法連線（網路/認證問題）: {e}")
        sys.exit(1)
    except ProgrammingError as e:
        logging.critical(f"權限或資料庫名稱錯誤: {e}")
        sys.exit(1)
    except Exception as e:
        logging.critical(f"發生未預期的資料庫錯誤: {e}")
        sys.exit(1)

# 取得Session方法
def get_session():
    """
    每次調用時，會從 engine 連線池中取出一個 Session。
    """
    with Session(engine) as session:
        yield session
