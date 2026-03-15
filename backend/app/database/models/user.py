from datetime import datetime
from typing import Optional, Any
from sqlmodel import SQLModel, Field, text

class User(SQLModel, table=True):
    __tablename__: Any = "users"
    student_id: str = Field(primary_key=True)
    display_name: str = Field(index=True, unique=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    role: str = Field(default="student")
    total_debt: int = Field(default=0)
    total_paid: int = Field(default=0)
    created_at: Optional[datetime] = Field(default=None)