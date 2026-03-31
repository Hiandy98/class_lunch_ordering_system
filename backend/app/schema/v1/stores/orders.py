from pydantic import BaseModel, ConfigDict
from typing import List

class OrderItem(BaseModel):
    name: str
    price: int


class StoreOrders(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    student_id: str
    content: List[OrderItem]
    total_price: int
    ...
