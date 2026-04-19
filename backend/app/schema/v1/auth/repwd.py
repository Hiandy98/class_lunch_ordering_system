from pydantic import BaseModel, ConfigDict

class Update(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    old_pwd: str
    new_pwd: str