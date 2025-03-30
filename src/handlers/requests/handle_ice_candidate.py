from models.Connection import Connection
from models.Peer import Peer
from models.Room import Room
from stores.rooms import rooms

async def handle_ice_candidate(reference_id: str, candidate: dict, connection: Connection):
    # Get peer
    peer: Peer = connection.peer

    # Get room
    room: Room = rooms[peer.room_id]

    # Get peer by reference_id
    peer_by_reference_id: Peer = room.peers[reference_id]

    # Set remote peer candidate
    await peer_by_reference_id.add_ice_candidate(ref_id=reference_id, candidate=candidate)
