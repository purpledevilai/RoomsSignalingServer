import asyncio
import uuid
from models.Connection import Connection
from stores.request_responses import request_responses
from rpc.models.request import Request


async def send_request(method: str, connection: Connection, params: dict = {}, await_response: bool = False):
    
    # Set request id if awaiting response
    request_id = None
    if await_response:
        request_id = str(uuid.uuid4())
        # Add request id to requests to await response
        request_responses[request_id] = None

    # Create request
    request = Request(method=method, params=params, request_id=request_id)

    # Send request
    await connection.websocket.send_json(request.model_dump())

    # If not awaiting response, return None
    if not await_response:
        return None
    
    # Await response
    while request_responses[request_id] == None:
        await asyncio.sleep(0.1)

    # Get response
    response = request_responses.pop(request_id)

    # Return data
    return response.data