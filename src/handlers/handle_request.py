from rpc.models.request import Request
from models.Connection import Connection
from lib.send_response import send_response
from handlers.requests.handle_join_room import handle_join_room
from handlers.requests.handle_request_connection import handle_request_connection
from handlers.requests.handle_ice_candidate import handle_ice_candidate

request_handler_registry = {
    "join": handle_join_room,
    "request_connection": handle_request_connection,
    "relay_ice_candidate": handle_ice_candidate,
}

async def handle_request(req: Request, connection: Connection):

    # Check if the request method is in the request_handler_registry
    if req.method not in request_handler_registry:
        raise Exception(f"Request method {req.method} not found")
    
    # Call the request handler
    handler_response = await request_handler_registry[req.method](**req.params, connection=connection)

    # If the request has a id, send the response
    if (req.id):
        await send_response(
            id=req.id,
            result=handler_response,
            connection=connection
        )