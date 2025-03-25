from rpc.models.request import Request
from models.Connection import Connection
from lib.send_response import send_response
from src.handlers.requests.handle_join_room import handle_join_room

request_handler_registry = {
    "handle_join_room": handle_join_room,
}

async def handle_request(req: Request, connection: Connection):

    # Check if the request method is in the request_handler_registry
    if req.method not in request_handler_registry:
        raise Exception(f"Request method {req.method} not found")
    
    # Call the request handler
    handler_response = await request_handler_registry[req.method](**req.params, connection=connection)

    # If the request has a request_id, send the response
    if (req.id):
        await send_response(req.id, handler_response, connection)