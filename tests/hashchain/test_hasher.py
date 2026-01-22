from mcp_audit_proxy.hashchain.hasher import compute_event_hash


def test_compute_event_hash_deterministic():
    event = {
        "trace_id": "trace-1",
        "event_seq": 1,
        "event_type": "request_received",
        "event_time": "2026-01-22T10:00:00Z",
        "prev_hash": "GENESIS",
    }

    h1 = compute_event_hash(event)
    h2 = compute_event_hash(event)

    assert h1 == h2
    assert len(h1) == 64
