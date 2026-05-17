from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List

class Update(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    is_active: Optional[bool] = None
    name: Optional[str] = None
    deadline: Optional[datetime] = None
    is_today_store: Optional[bool] = None
    menu_url: Optional[List[str]] = None