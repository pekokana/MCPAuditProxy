import pytest
from mcp_audit_proxy.hashchain.hasher import compute_event_hash
from mcp_audit_proxy.hashchain.verifier import (
    verify_hash_chain,
    HashChainVerificationError,
)


def test_verify_chain_with_restart():
    """正常系：再起動イベントを含むチェーン"""
    events = []
    prev_hash = "GENESIS"

    # --- first segment ---
    for seq in range(1, 3):
        e = {
            "trace_id": "trace-1",
            "event_seq": seq,
            "event_type": "event",
            "event_time": f"2026-01-22T10:00:0{seq}Z",
            "prev_hash": prev_hash,
        }
        e["hash"] = compute_event_hash(e)
        prev_hash = e["hash"]
        events.append(e)

    # --- restart segment ---
    chain_start = {
        "trace_id": "_system",
        "event_seq": 1,
        "event_type": "chain_start",
        "event_time": "2026-01-22T11:00:00Z",
        "prev_hash": prev_hash,
    }
    chain_start["hash"] = compute_event_hash(chain_start)
    prev_hash = chain_start["hash"]
    events.append(chain_start)

    # --- second segment ---
    e = {
        "trace_id": "trace-2",
        "event_seq": 2,
        "event_type": "event",
        "event_time": "2026-01-22T11:00:01Z",
        "prev_hash": prev_hash,
    }
    e["hash"] = compute_event_hash(e)
    events.append(e)

    verify_hash_chain(events)


def test_missing_chain_start_is_detected():
    """異常系：再起動イベントを消すと検知される"""
    events = []
    prev_hash = "GENESIS"

    # first segment
    for seq in range(1, 4):
        e = {
            "trace_id": "trace-1",
            "event_seq": seq,
            "event_type": "event",
            "event_time": f"2026-01-22T10:00:0{seq}Z",
            "prev_hash": prev_hash,
        }
        e["hash"] = compute_event_hash(e)
        prev_hash = e["hash"]
        events.append(e)

    # 改ざん：seq リセットで chain_start を偽装
    events[2]["event_seq"] = 1

    with pytest.raises(HashChainVerificationError):
        verify_hash_chain(events)
