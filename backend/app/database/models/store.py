from uuid import UUID
from datetime import datetime
from typing import Optional, List, Any
from sqlmodel import SQLModel, Field, text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import Column, String

class Store(SQLModel, table=True):
    __tablename__: Any = "stores"
    id: Optional[UUID] = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={
            "server_default": text("gen_random_uuid()"),
            "nullable": False
        }
    )
    name: Optional[str] = Field(default=None)
    menu_url: Optional[List[str]] = Field(default_factory=list, sa_column=Column(ARRAY(String)))
    is_active: bool = Field(default=True)
    deadline: Optional[datetime] = Field(default=None)
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column_kwargs={"server_default": text("now()")}
    )