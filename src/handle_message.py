import json
from models.Connection import Connection
from rpc.models import response, request
from handlers.handle_request import handle_request
from handlers.handle_response import handle_response


async def handle_message(connection: Connection, message: str):
    try:
        # Parse the JSON message
        data = json.loads(message)
        print("received message", data)

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
            print("received request", req.model_dump())
            await handle_request(req, connection)

        # Response
        if (type == "response"):
            res = response.Response(**data)
            print("received response", res.model_dump())
            handle_response(res)

    except Exception as e:
        print(f"\nError handling message\nMESSAGE\n{message}\nERROR\n{e}\n")
        await connection.websocket.send_json({"type": "error", "error": str(e)})
