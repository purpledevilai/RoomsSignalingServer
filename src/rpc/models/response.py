from pydantic import BaseModel

class Response(BaseModel):
    request_id: str
    data: dict
    type: str = "response"
