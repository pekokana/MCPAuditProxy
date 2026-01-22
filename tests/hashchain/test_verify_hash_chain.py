import pytest

from mcp_audit_proxy.hashchain.hasher import compute_event_hash
from mcp_audit_proxy.hashchain.verifier import (
    verify_hash_chain,
    HashChainVerificationError,
)


def build_event(trace_id, seq, prev_hash):
    event = {
        "trace_id": trace_id,
        "event_seq": seq,
        "event_type": "test_event",
        "event_time": f"2026-01-22T10:00:0{seq}Z",
        "prev_hash": prev_hash,
    }
    event["hash"] = compute_event_hash(event)
    return event


def test_verify_valid_chain():
    """正常系：正しいチェーンは例外を出さない"""
    events = []

    prev_hash = "GENESIS"
    for seq in range(1, 4):
        event = build_event("trace-1", seq, prev_hash)
        prev_hash = event["hash"]
        events.append(event)

    # 例外が出なければ成功
    verify_hash_chain(events)


def test_detect_tampering():
    """異常系：改ざんを検知して例外を送出する"""
    events = []

    prev_hash = "GENESIS"
    for seq in range(1, 3):
        event = build_event("trace-1", seq, prev_hash)
        prev_hash = event["hash"]
        events.append(event)

    # 改ざん（prev_hash を壊す）
    events[1]["prev_hash"] = "INVALID_HASH"

    with pytest.raises(HashChainVerificationError):
        verify_hash_chain(events)
