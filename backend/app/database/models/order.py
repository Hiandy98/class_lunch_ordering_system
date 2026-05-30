from uuid import UUID
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlmodel import SQLModel, Field, text
from sqlalchemy.dialects.postgresql import JSONB

class Order(SQLModel, table=True):
    __tablename__: Any = "orders"
    id: Optional[UUID] = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={
            "server_default": text("gen_random_uuid()"),
            "nullable": False
        }
    )
    student_id: str = Field(foreign_key="users.student_id")
    store_id: UUID = Field(foreign_key="stores.id")
    content: List[Dict[str, Any]] = Field(default_factory=list, sa_type=JSONB)
    total_price: int = Field(default=0)
    is_active: bool = Field(default=False)
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column_kwargs={"server_default": text("now()")}
    )
    is_locked: bool = Field(default=False)