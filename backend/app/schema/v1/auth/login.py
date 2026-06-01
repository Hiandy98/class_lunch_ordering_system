from pydantic import BaseModel, ConfigDict
from typing import Optional

class Login(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    state: str
    token: Optional[str] = None