# ファイル名: test_audit_events_sample.py
# 配置場所: mcp_audit_proxy/tests/

import json
import pytest
from pathlib import Path

from mcp_audit_proxy.hashchain.hasher import compute_event_hash
from mcp_audit_proxy.hashchain.verifier import verify_hash_chain, HashChainVerificationError


def load_sample_events():
    """samples/audit_events_with_chain_start.json を読み込む"""
    samples_path = Path(__file__).parent.parent / "samples" / "audit_events_with_chain_start.json"
    with open(samples_path, "r", encoding="utf-8") as f:
        events = json.load(f)
    return events


def test_sample_audit_chain_valid():
    """chain_start を含むサンプルイベントのハッシュチェーン検証"""
    events = load_sample_events()

    # 実際にハッシュを計算して更新
    prev_hash = "GENESIS"
    for event in events:
        event["this_hash"] = compute_event_hash({
            "trace_id": event["trace_id"],
            "event_seq": event["event_seq"],
            "event_type": event["event_type"],
            "event_time": event["event_time"],
            "prev_hash": prev_hash,
        })
        prev_hash = event["this_hash"]

    # 例外が出なければ検証成功
    verify_hash_chain(events)


def test_sample_audit_chain_tampering_detected():
    """改ざんを検知できることを確認"""
    events = load_sample_events()

    # 正常なハッシュを計算
    prev_hash = "GENESIS"
    for event in events:
        event["this_hash"] = compute_event_hash({
            "trace_id": event["trace_id"],
            "event_seq": event["event_seq"],
            "event_type": event["event_type"],
            "event_time": event["event_time"],
            "prev_hash": prev_hash,
        })
        prev_hash = event["this_hash"]

    # 改ざん: 2つ目のイベントの prev_hash を壊す
    events[1]["prev_hash"] = "INVALID_HASH"

    with pytest.raises(HashChainVerificationError):
        verify_hash_chain(events)
