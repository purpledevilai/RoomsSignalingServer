from pydantic import BaseModel
from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from models.Peer import Peer  # imported only for type hints

from lib.connect_peers import connect_peers

class Room(BaseModel):
    room_id: str
    # Forward-reference "Peer" to avoid importing it at runtime
    peers: Dict[str, "Peer"] = {}

    async def add_peer(self, peer: "Peer"):
        # If there are no others in the room, just add and return
        print("length of peers", len(self.peers))
        if len(self.peers) == 0:
            print("adding first peer to empty room")
            self.peers = {peer.id: peer}
            return
        
        # Otherwise establish connections with each peer
        for other_peer in self.peers.values():
            print(f"Connecting Peers {other_peer.id} and {peer.id}")
            await connect_peers(peer, other_peer)
        
        # Add the new peer to the list
        print("adding peer to room")
        self.peers[peer.id] = peer

    async def remove_peer(self, peer: "Peer"):
        # Remove peer from list
        self.peers.pop(peer.id)
