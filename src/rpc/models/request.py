from pydantic import BaseModel
from typing import Optional

class Request(BaseModel):
    id: Optional[str] = None
    method: str
    params: Optional[dict] = {}