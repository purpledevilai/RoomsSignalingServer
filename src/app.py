from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from models import Connection
from handle_message import handle_message

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

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    # Accept the WebSocket connection
    await websocket.accept()
    print("Connection opened")

    # Create a Connection object
    connection = Connection.Connection(websocket=websocket)

    try:
        # Handle messages
        while True:
            message = await websocket.receive_text()
            await handle_message(connection, message)

    except WebSocketDisconnect:
        print("Connection closed")

    except Exception as e:
        print("There was an error with the WebSocket connection:", e)

    finally:
        await websocket.close()
