from uuid import UUID
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlmodel import SQLModel, Field
from sqlalchemy.dialects.postgresql import JSONB

class Order(SQLModel, table=True):
    __tablename__: Any = "orders"
    id: Optional[UUID] = Field(default=None, primary_key=True)
    student_id: str = Field(foreign_key="users.student_id")
    store_id: UUID = Field(foreign_key="stores.id")
    content: List[Dict[str, Any]] = Field(default_factory=list, sa_type=JSONB)
    total_price: int = Field(default=0)
    is_paid: bool = Field(default=False)
    created_at: Optional[datetime] = Field(default=None)