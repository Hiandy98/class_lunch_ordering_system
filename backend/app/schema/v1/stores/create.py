from pydantic import BaseModel, ConfigDict
from uuid import UUID


class StoreCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str

class Create(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    id: UUID
