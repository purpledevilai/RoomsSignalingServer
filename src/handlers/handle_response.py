from rpc.models.response import Response
from stores.request_responses import request_responses

def handle_response(res: Response):

    # Check if the request id is in the request_responses
    if res.id not in request_responses:
        raise Exception(f"Request id {res.request_id} not found")
    
    # Add the response to the request_responses
    request_responses[res.id] = res