import json
from models import Connection
from rpc.models import response, request
from handlers.handle_request import handle_request
from handlers.handle_response import handle_response


async def handle_message(connection: Connection.Connection, message: str):
    try:
        # Parse the JSON message
        data = json.loads(message)

        # Get the message type
        type = data.get("type")
        if (type == None):
            raise Exception("No type provided")
        
        # Check if the type is request or response
        if (type != "request" and type != "response"):
            raise Exception("Invalid type provided")
        
        # Request
        if (type == "request"):
            req = request.Request(**data)
            await handle_request(req, connection)

        # Response
        if (type == "response"):
            res = response.Response(**data)
            await handle_response(res)

    except Exception as e:
        print(f"Error: {e}")
        await connection.websocket.send_json({"type": "error", "error": str(e)})
