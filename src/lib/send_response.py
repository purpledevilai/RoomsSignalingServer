from models.Connection import Connection
from rpc.models.response import Response

async def send_response(id: str, result: dict, connection: Connection):
    response = Response(id=id, result=result)
    print("sending response", response.model_dump())
    await connection.websocket.send_json(response.model_dump())