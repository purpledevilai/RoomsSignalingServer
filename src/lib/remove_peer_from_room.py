from models.Peer import Peer
from stores.rooms import rooms
from stores.connections import connections

async def remove_peer_from_room(peer: Peer):
    room = rooms[peer.room_id]
    await room.remove_peer(peer)
    connection = connections[peer.connection_id]
    await connection.websocket.close()
    if len(room.peers) == 0:
        print("Removing room as no peers remain")
        rooms.pop(peer.room_id)