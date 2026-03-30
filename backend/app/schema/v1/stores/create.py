from pydantic import BaseModel, ConfigDict
from typing import List


class StoreCreate(BaseModel):
    name: str
    menu_url: List[str]

class Create(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    menu_url: list[str]
