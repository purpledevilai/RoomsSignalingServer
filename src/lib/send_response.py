from models.Connection import Connection
from rpc.models.response import Response

async def send_response(request_id: str, data: dict, connection: Connection):
    response = Response(request_id=request_id, data=data)
    print("sending response", response.model_dump())
    await connection.websocket.send_json(response.model_dump())