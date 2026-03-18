from pydantic import BaseModel, ConfigDict
from typing import Any, Dict, List
from uuid import UUID

class OrderItem(BaseModel):
    name: str
    price: int


class AllOrder(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    student_id: str
    store_id: UUID
    content: List[OrderItem]
    total_price: int
    is_paid: bool
    ...


