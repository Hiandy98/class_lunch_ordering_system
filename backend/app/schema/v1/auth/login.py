from pydantic import BaseModel

class Login(BaseModel):
    state: str