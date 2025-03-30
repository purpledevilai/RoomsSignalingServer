from models.Peer import Peer

async def connect_peers(peer_a: Peer, peer_b: Peer):

    # Create first RTC connection
    offer = await peer_a.create_rtc_peer_connection_and_offer(ref_id=peer_b.id)
    print("CREATED OFFER FOR PEER A")

    # Create answer from first peer's offer
    answer = await peer_b.create_rtc_peer_connection_and_answer(ref_id=peer_a.id, offer=offer)
    print("CREATED ANSWER FOR PEER B")

    # Set the answer on the first peer
    await peer_a.set_remote_peer_answer(ref_id=peer_b.id, answer=answer)
    print("SET ANSWER FOR PEER A")



    