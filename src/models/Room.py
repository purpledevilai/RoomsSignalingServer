from pydantic import BaseModel
from typing import TYPE_CHECKING, Dict
from lib.send_request import send_request
from stores.connections import connections

if TYPE_CHECKING:
    from models.Peer import Peer  # imported only for type hints

class Room(BaseModel):
    room_id: str
    peers: Dict[str, "Peer"] = {}

    async def add_peer(self, peer: "Peer"):
        # If there are no others in the room, just add and return
        print("length of peers", len(self.peers))
        if len(self.peers) == 0:
            print("adding first peer to empty room")
            self.peers = {peer.id: peer}
            return
        
        # Otherwise aleart the new peer to all other peers
        for other_peer in self.peers.values():
            print(f"Alerting peer {other_peer.id} to new peer {peer.id}")
            # Get other peer connection to send the request
            connection = connections[other_peer.connection_id]

            # Check other peer connection
            if connection is None:
                raise Exception(f"Connection with id {other_peer.connection_id} does not exist. Attempting to request connection")
            
            # Send the new peer to the other peer connection
            await send_request(
                method="peer_added",
                params={
                    "peer_id": peer.id,
                    "self_description": peer.self_description,
                },
                connection=connection
            )
        
        # Add the new peer to the list
        print("adding peer to room")
        self.peers[peer.id] = peer

    async def remove_peer(self, peer: "Peer"):
        # Remove peer from list
        self.peers.pop(peer.id)
