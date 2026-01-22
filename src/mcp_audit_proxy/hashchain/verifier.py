from .hasher import compute_event_hash


class HashChainVerificationError(Exception):
    pass


def verify_hash_chain(events: list[dict]) -> None:
    if not events:
        return

    prev_event = None

    for event in events:
        if event.get("hash") != compute_event_hash(event):
            raise HashChainVerificationError("Hash mismatch")

        if prev_event:
            if event["prev_hash"] != prev_event["hash"]:
                raise HashChainVerificationError("prev_hash mismatch")

            if event["event_type"] == "chain_start":
                if event["event_seq"] != 1:
                    raise HashChainVerificationError("chain_start seq must be 1")
            else:
                if event["event_seq"] != prev_event["event_seq"] + 1:
                    raise HashChainVerificationError("event_seq broken")
        else:
            if event["prev_hash"] != "GENESIS":
                raise HashChainVerificationError("Invalid chain start")

        prev_event = event
