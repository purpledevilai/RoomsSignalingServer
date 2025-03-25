from pydantic import BaseModel
from models.Peer import Peer
from lib.connect_peers import connect_peers

class Room(BaseModel):
    room_id: str
    peers: list[Peer] = []

    async def add_peer(self, peer: Peer):
        # If there are no others in the room, just add and return
        if (len(self.peers) == 0):
            self.peers = [peer]
            return
        
        # Otherwise establish connections with each peer
        for other_peer in self.peers:
            await connect_peers(peer, other_peer)
        
        # Add the new peer to the list
        self.peers.append(peer)