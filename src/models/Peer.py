from pydantic import BaseModel
from lib.send_request import send_request
from stores.connections import connections


class Peer(BaseModel):
    id: str
    connection_id: str
    self_description: str
    room_id: str

    async def create_rtc_peer_connection_and_offer(self, ref_id: str) -> dict:
        print("Sending create_rtc_peer_connection_and_offer request")
        offer_data = await send_request(
            method="create_rtc_peer_connection_and_offer",
            params={"ref_id": ref_id},
            await_response=True,
            connection=connections[self.connection_id]
        )
        print("Received offer_data", offer_data)
        return offer_data["offer"]

    async def create_rtc_peer_connection_and_answer(self, ref_id: str, offer: dict) -> dict:
        print("Sending create_rtc_peer_connection_and_answer request")
        answer_data = await send_request(
            method="create_rtc_peer_connection_and_answer",
            params={"ref_id": ref_id, "offer": offer},
            await_response=True,
            connection=connections[self.connection_id]
        )
        print("Received answer data", answer_data)
        return answer_data["answer"]

    async def set_remote_peer_answer(self, ref_id: str, answer: dict):
        print("Sending set_remote_peer_answer request")
        await send_request(
            method="set_remote_peer_answer",
            params={"ref_id": ref_id, "answer": answer},
            await_response=False,
            connection=connections[self.connection_id]
        )

    async def add_ice_candidate(self, ref_id: str, candidate: dict):
        print("Sending add_ice_candidate request")
        await send_request(
            method="add_ice_candidate",
            params={"ref_id": ref_id, "candidate": candidate},
            await_response=False,
            connection=connections[self.connection_id]
        )