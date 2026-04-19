from pydantic import BaseModel, ConfigDict

class Update(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    display_name: str