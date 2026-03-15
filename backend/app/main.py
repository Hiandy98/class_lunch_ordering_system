import logging
from utils.logger import LoggerParameter, Logger


def main():
    log_params = LoggerParameter(
        AI_instructions="""
        [PROJECT CONTEXT]
        Name: class_lunch_ordering_system
        Goal: 一個班級的訂餐系統 在此輸出後端運行日誌
        """,
        logging_level="DEBUG",
        do_session_log= True,
        do_console_log= True,
        do_master_log = False,
    )

    Logger.init(log_params)

    logging.info("進行連線測試")
    import database.session
    database.session.connect_check()


    logging.info("Hello from class-lunch-ordering-system V0.0-Beta")

    # from lab.db_connent_test1 import test_user_operations
    # try:
    #     test_user_operations()
    # except Exception as e:
    #     print(f"s發生錯誤：{e}")

    

if __name__ == "__main__":
    main()
