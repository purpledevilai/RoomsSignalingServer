# models/__init__.py
from .Connection import Connection
from .Peer import Peer
from .Room import Room

# Now rebuild them after all are imported
Connection.model_rebuild()
Peer.model_rebuild()
Room.model_rebuild()