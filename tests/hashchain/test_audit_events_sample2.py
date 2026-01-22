import json
import pytest
from pathlib import Path
from mcp_audit_proxy.hashchain.verifier import verify_hash_chain, HashChainVerificationError

SAMPLES_DIR = Path(__file__).parent.parent.parent / "samples"

def load_sample_events(filename="audit_events_with_chain_start.json"):
    path = SAMPLES_DIR / filename
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def test_sample_chain():
    """正常系：サンプルチェーンが正しく検証される"""
    events = load_sample_events()
    verify_hash_chain(events)

def test_tampered_chain():
    """異常系：サンプルチェーンを改ざんして検知"""
    events = load_sample_events()
    # 改ざん
    events[1]["prev_hash"] = "INVALID_HASH"

    with pytest.raises(HashChainVerificationError):
        verify_hash_chain(events)
