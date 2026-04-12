from datetime import datetime
from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional

class AllStore(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    name: str
    is_today_store: bool
    is_active: bool
    deadline: Optional[datetime] = None 
    ...