import os
import logging
import asyncio
from anyio import to_thread
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHashError
from dotenv import load_dotenv

load_dotenv()
password_key = os.getenv("PASSWORD_KEY")
if not password_key:
    logging.warning("環境變數 PASSWORD_KEY 缺失! 將不採用此項目")


password_hasher = PasswordHasher(
    memory_cost=16384,
    time_cost=2,
    parallelism=1
)

# 防止每次驗證要16MB記憶體 同時登入造成的開銷
password_limit = asyncio.Semaphore(4)


def _create_hash_pwd(user_id: str, original_password: str) -> str:
    if not password_key:
        target_password = original_password
    else:
        target_password = original_password + password_key
    password = password_hasher.hash(target_password)
    logging.debug(f"正在為{user_id}建立安全密碼")
    return password

def _verify_password(user_id: str, hashed_password: str, input_password: str) -> bool:
    try:
        if password_key:
            target_password = input_password + password_key
        else:
            target_password = input_password
        logging.debug(f"正在為{user_id}進行登入驗證")
        return password_hasher.verify(hashed_password, target_password)
    except VerifyMismatchError:  # 輸入錯誤密碼
        logging.debug(f"用戶{user_id}登入密碼錯誤")
        return False
    except (InvalidHashError, Exception) as e:
        logging.warning(f"安全警告或系統錯誤: {e}")
        return False


async def safe_create_password(user_id: str, original_password: str) -> str:
    async with password_limit:
        return await to_thread.run_sync(
            _create_hash_pwd, user_id, original_password
        )
    
async def safe_verify_password(user_id: str, hash_pwd: str, input_pwd: str) -> bool:
    async with password_limit:
        return await to_thread.run_sync(
            _verify_password, user_id, hash_pwd, input_pwd
        )

async def test():
    pwd = await safe_create_password("140252", "140252")
    print(pwd)

if __name__ == "__main__":
    asyncio.run(test())