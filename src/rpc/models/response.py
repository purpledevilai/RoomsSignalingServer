from pydantic import BaseModel

class Response(BaseModel):
    id: str
    result: dict