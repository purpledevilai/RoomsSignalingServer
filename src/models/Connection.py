from pydantic import BaseModel
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    # Only imported for type hints, not at runtime
    from models.Peer import Peer

class Connection(BaseModel):
    id: str
    websocket: object
    # Use forward reference for Peer
    peer: Optional["Peer"] = None