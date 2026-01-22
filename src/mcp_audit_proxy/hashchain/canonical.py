import json
from typing import Dict, Any


def canonical_json(data: Dict[str, Any]) -> str:
    """
    Canonical JSON:
    - keys sorted
    - no null values
    - compact separators
    """
    filtered = {k: v for k, v in data.items() if v is not None}

    return json.dumps(
        filtered,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
