from pydantic import BaseModel, ConfigDict
from uuid import UUID

class AllStore(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    name: str
    is_today_store: bool
    is_active: bool
    # 其餘愈傳遞參數
    ...