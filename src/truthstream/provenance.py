"""Evidence provenance assessment for TruthStream outputs.

A confidence score is not proof. Source-backed status requires resolvable source
URLs, retrieval timestamps, and stable evidence identifiers for every cited item.
"""
from __future__ import annotations

from datetime import datetime
from urllib.parse import urlparse
from typing import Any


def is_source_backed_evidence(item: dict[str, Any]) -> bool:
    source = item.get("source")
    if not isinstance(source, dict):
        return False
    url = source.get("url")
    evidence_id = item.get("evidence_id")
    retrieved_at = item.get("retrieved_at")
    if not isinstance(url, str) or not isinstance(evidence_id, str) or not evidence_id.strip():
        return False
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.netloc:
        return False
    if not isinstance(retrieved_at, str) or not retrieved_at.strip():
        return False
    try:
        datetime.fromisoformat(retrieved_at.replace("Z", "+00:00"))
    except ValueError:
        return False
    return True


def provenance_summary(result: dict[str, Any]) -> dict[str, Any]:
    """Classify the provenance completeness of a serialized verification result."""
    groups = (
        "supporting_evidence",
        "contradicting_evidence",
        "neutral_evidence",
    )
    items: list[dict[str, Any]] = []
    for key in groups:
        value = result.get(key, [])
        if isinstance(value, list):
            items.extend(item for item in value if isinstance(item, dict))
    if not items:
        return {
            "status": "no_evidence",
            "evidence_count": 0,
            "source_count": 0,
            "verified_items": 0,
        }
    verified = [item for item in items if is_source_backed_evidence(item)]
    urls = {
        item["source"]["url"]
        for item in verified
        if isinstance(item.get("source"), dict)
    }
    complete = len(verified) == len(items)
    return {
        "status": "source_backed" if complete else "demo_or_incomplete",
        "evidence_count": len(items),
        "source_count": len(urls),
        "verified_items": len(verified),
    }
