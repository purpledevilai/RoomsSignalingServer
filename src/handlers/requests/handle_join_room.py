from stores.rooms import rooms
from models.Connection import Connection
from models.Room import Room
from models.Peer import Peer


async def handle_join_room(room_id: str, connection: Connection):
    # Check for room_id
    if room_id == None:
        raise Exception("No room_id provided")
    
    # Check if room_id is in rooms
    if room_id not in rooms:
        rooms[room_id] = Room(room_id=room_id)

    # Get room
    room = rooms[room_id]

    # Create peer
    peer = Peer(connection=connection, room=room)

    # Set peer on connection
    connection.peer = peer

    # Add peer to room
    await room.add_peer(peer)

    return {"success": True}


    

