from pydantic import BaseModel
import uuid
from models.Connection import Connection
from models.Room import Room
from lib.send_request import send_request

class Peer(BaseModel):
    id: str
    connection: Connection
    room: Room

    def __init__(self, connection: Connection, room: Room):
        self.id = str(uuid.uuid4())
        self.connection = connection
        self.room = room

    async def create_rtc_peer_connection_and_offer(self, ref_id: str) -> dict:
        offer = await send_request(
            method="create_rtc_peer_connection_and_offer",
            params={
                "ref_id": ref_id
            },
            await_response=True,
            connection=self.connection
        )
        return offer
    
    async def create_rtc_peer_connection_and_answer(self, ref_id: str, offer: dict) -> dict:
        answer = await send_request(
            method="create_rtc_peer_connection_and_answer",
            params={
                "ref_id": ref_id,
                "offer": offer
            },
            await_response=True,
            connection=self.connection
        )
        return answer
    
    async def set_remote_peer_answer(self, ref_id: str, answer: dict):
        await send_request(
            method="set_remote_peer_answer",
            params={
                "ref_id": ref_id,
                "answer": answer
            },
            await_response=False,
            connection=self.connection
        )

    
