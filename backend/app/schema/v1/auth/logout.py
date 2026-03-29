from pydantic import BaseModel

class Logout(BaseModel):
    state: str