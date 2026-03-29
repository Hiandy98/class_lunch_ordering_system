from pydantic import BaseModel

class VerifyToken(BaseModel):
    user_id: str
    display_name: str
    role: str
    status: str