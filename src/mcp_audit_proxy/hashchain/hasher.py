import hashlib
from typing import Dict

from .canonical import canonical_json


def compute_event_hash(event: Dict) -> str:
    """
    Compute SHA-256 hash of a canonicalized audit event.
    """
    canonical = canonical_json(event)
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return digest
