from stores.rooms import rooms
from models.Connection import Connection
from models.Room import Room
from models.Peer import Peer
import uuid


async def handle_join_room(room_id: str, self_description: str, connection: Connection):
    # Check for room_id
    if room_id == None:
        raise Exception("No room_id provided")

    # Check if room_id is in rooms
    print("Rooms", rooms)
    if room_id not in rooms:
        rooms[room_id] = Room(room_id=room_id)
        print("Room created", rooms[room_id])

    # Get room
    room = rooms[room_id]

    # Create peer
    peer = Peer(id=str(uuid.uuid4()), self_description=self_description, connection_id=connection.id, room_id=room_id)
    print("Peer created", peer)

    # Set peer on connection
    connection.peer = peer

    # Add peer to room
    print("Adding peer to room")
    await room.add_peer(peer)


    return {"success": True}
