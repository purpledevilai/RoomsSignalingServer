from stores.rooms import rooms
from models.Connection import Connection
from stores.connections import connections
from lib.send_request import send_request


async def handle_request_connection(peer_id: str, self_description: str, offer: dict, connection: Connection):

    # Check peer
    if (not connection.peer):
        raise Exception("Connection does not contain a peer")
    
    # Get the room
    room = rooms[connection.peer.room_id]
    
    # Check room
    if (not room):
        raise Exception(f"Room with id {connection.peer.room_id} does not exist")

    # Get the requestee peer
    requestee_peer = room.peers[peer_id]

    # Check requestee peer
    if (not requestee_peer):
        raise Exception(f"Peer with id {peer_id} does not exist in room {connection.peer.room_id}")
    
    # Get the requestee peer connection to send the message
    requestee_connection = connections[requestee_peer.connection_id]

    # Check the connection
    if (not requestee_connection):
        raise Exception(f"Connection with id {requestee_peer.connection_id} does not exist. Attempting to request connection")

    # Send requestee peer connection request
    print("Sending connection request")
    answer = await send_request(
        method="connection_request",
        params={
            "peer_id": connection.peer.id,
            "self_description": self_description,
            "offer": offer,
        },
        connection=requestee_connection,
        await_response=True
    )
    print("Received answer data", answer)

    # Check answer
    if (not answer):
        raise Exception("No answer received from requestee peer")
    
    # Return answer
    return {
        "answer": answer,
    }