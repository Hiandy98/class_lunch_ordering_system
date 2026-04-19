from pydantic import BaseModel, ConfigDict
from typing import List
from uuid import UUID

class OrderItem(BaseModel):
    name: str
    price: int


class StoreOrders(BaseModel):
    id: UUID
    model_config = ConfigDict(from_attributes=True)
    student_id: str
    content: List[OrderItem]
    total_price: int
    is_active: bool
    ...
