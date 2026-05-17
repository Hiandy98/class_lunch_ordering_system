from pydantic import BaseModel, ConfigDict
from typing import List

class Url(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    menu_url: List[str]
    ...