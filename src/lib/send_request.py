import asyncio
import uuid
from models.Connection import Connection
from stores.request_responses import request_responses
from rpc.models.request import Request


async def send_request(method: str, connection: Connection, params: dict = {}, await_response: bool = False, timeout_seconds: int = 10):
    # Set request id if awaiting response
    request_id = None
    if await_response:
        request_id = str(uuid.uuid4())
        # Add request id to requests to await response
        request_responses[request_id] = None

    # Create request
    request = Request(method=method, params=params, id=request_id)
    print(f"Sending request", request.model_dump())
    
    # Send request
    await connection.websocket.send_json(request.model_dump())

    # If not awaiting response, return None
    if not await_response:
        return None
    
    # Await response
    elapsed_time = 0
    interval = 0.1
    while request_responses[request_id] == None and elapsed_time < timeout_seconds:
        elapsed_time += interval
        await asyncio.sleep(interval)

    # Check if request timed out
    if request_responses[request_id] == None:
        # Remove request id from requests to await response
        del request_responses[request_id]
        raise Exception(f"Request with id {request_id} timed out after {timeout_seconds} seconds")

    # Get response
    response = request_responses.pop(request_id)
    print(f"Received response", response.model_dump())

    # Return data
    return response.result