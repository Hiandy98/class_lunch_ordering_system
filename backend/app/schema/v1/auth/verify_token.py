from pydantic import BaseModel, ConfigDict

class VerifyToken(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: str
    display_name: str
    role: str
    status: str