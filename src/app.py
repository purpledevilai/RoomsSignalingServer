from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from models.Connection import Connection
from stores.connections import connections
from handle_message import handle_message
import uuid
from lib.remove_peer_from_room import remove_peer_from_room
from stores.rooms import rooms

app = FastAPI()

# Optional: Add CORS if you expect to call from other domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check
@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/reset/{room_id}")
async def reset_room(room_id: str):
    # Check if the room exists
    room = rooms.get(room_id)
    if not room:
        return {"Error": "room room_id does not exist"}

    # Remove all peers from the room
    peers_to_remove = list(room.peers.values())  # Copy to avoid modification during iteration
    for peer in peers_to_remove:
        await remove_peer_from_room(peer)

    return {"status": "room reset successfully"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    # Accept the WebSocket connection
    await websocket.accept()
    print("Connection opened")

    # Create a Connection object
    connection_id = str(uuid.uuid4())
    connection = Connection(id=connection_id, websocket=websocket)
    connections[connection_id] = connection

    try:
        # Handle messages
        while True:
            message = await websocket.receive_text()
            asyncio.create_task(handle_message(connection, message))

    except WebSocketDisconnect:
        print("Connection closed")

    except Exception as e:
        print("There was an error with the WebSocket connection:", e)

    finally:
        if connection.peer:
            await remove_peer_from_room(connection.peer)
        try:
            await websocket.close()
        except:
            pass
