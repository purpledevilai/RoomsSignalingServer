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
        
        # Request
        if ("method" in data):
            req = request.Request(**data)
            print("received request", req.model_dump())
            await handle_request(req, connection)

        # Response
        elif ("result" in data):
            res = response.Response(**data)
            print("received response", res.model_dump())
            handle_response(res)

        # Not recognised
        else:
            raise Exception("Message not recognised")

    except Exception as e:
        print(f"\nError handling message\nMESSAGE\n{message}\nERROR\n{e}\n")
        await connection.websocket.send_json({"type": "error", "error": str(e)})
