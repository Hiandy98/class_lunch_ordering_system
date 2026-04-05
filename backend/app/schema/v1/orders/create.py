from pydantic import BaseModel, ConfigDict
from typing import List
from uuid import UUID


class OrderItem(BaseModel):
    name: str
    price: int


class OrderCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    store_id: UUID
    content: List[OrderItem]
    total_price: int
    is_active: bool