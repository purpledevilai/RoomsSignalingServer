from pydantic import BaseModel
from typing import Optional
from models.Peer import Peer

class Connection(BaseModel):
    websocket: object
    peer: Optional[Peer] = None