from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional, List

class AllStore(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    name: str
    menu_url: Optional[List[str]]
    # 其餘愈傳遞參數
    ...