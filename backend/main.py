import logging
from app.utils.logger import LoggerParameter, Logger
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.v1 import api_v1_router


log_params = LoggerParameter(
    AI_instructions="""
    [PROJECT CONTEXT]
    Name: class_lunch_ordering_system
    Goal: 一個班級的訂餐系統 在此輸出後端運行日誌
    """,
    logging_level="DEBUG",
    do_session_log=True,
    do_console_log=True,
    do_master_log=False,
)


def main():
    Logger.init(log_params)
    
    logging.info("進行連線測試")
    from app.database.session import connect_check
    connect_check()
    
    logging.info("Hello from class-lunch-ordering-system V0.0-Beta")


# 防止啟動後跟不上伺服器 在uvicorn控制中啟動main()函式
@asynccontextmanager
async def lifespan(app: FastAPI):
    main()
    yield


# FastAPI 設定區域
app = FastAPI(title="Test", lifespan=lifespan)
app.include_router(api_v1_router)

@app.get("/")
def root():
    return {"message": "Success"}


# 入口
if __name__ == "__main__":
    import uvicorn
    logging.info("正在開啟伺服器")
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
    logging.info("正在關閉開啟伺服器")
