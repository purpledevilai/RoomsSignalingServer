from models.Connection import Connection
from stores.connections import connections
from models.Peer import Peer
from models.Room import Room
from stores.rooms import rooms
from lib.send_request import send_request

async def handle_ice_candidate(peer_id: str, candidate: dict, connection: Connection):
    # Get peer for the room
    peer: Peer = connection.peer

    # Check peer
    if peer is None:
        raise Exception("Peer not found in connection")

    # Get room for the callee peer
    room: Room = rooms[peer.room_id]

    # Check room
    if room is None:
        raise Exception(f"Room with id {peer.room_id} does not exist")
    
    # Check if callee peer_id is in room
    if peer_id not in room.peers:
        raise Exception(f"Peer with id {peer_id} does not exist in room {peer.room_id}")
    
    # Get callee peer by id to send the ICE candidate to
    callee_peer: Peer = room.peers[peer_id]
    print("Callee peer", callee_peer)

    # Get callee peer connection to send the request
    callee_connection: Connection = connections[callee_peer.connection_id]

    # Check callee connection
    if callee_connection is None:
        raise Exception(f"Connection with id {callee_peer.connection_id} does not exist. Attempting to request connection")
    
    # Send the ICE candidate to the callee connection
    print("Sending ICE candidate")
    await send_request(
        method="add_ice_candidate",
        params={
            "peer_id": peer.id,
            "candidate": candidate,
        },
        connection=callee_connection,
        await_response=False
    )
    print("Sent ICE candidate")
