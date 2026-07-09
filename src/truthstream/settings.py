"""Runtime settings helpers for TruthStream."""

from __future__ import annotations

import os
from typing import Literal

from truthstream.evidence import (
    EvidenceRetriever,
    InMemoryEvidenceRetriever,
    real_evidence_retriever,
)

EvidenceMode = Literal["demo", "real"]


def build_evidence_retriever(mode: EvidenceMode | None = None) -> EvidenceRetriever:
    """Build the configured evidence retriever.

    `demo` preserves the deterministic v0.1 behavior. `real` enables the Wikipedia, Crossref,
    and OpenAlex provider stack.
    """

    selected_mode = mode or os.getenv("TRUTHSTREAM_EVIDENCE_MODE", "demo").lower()
    if selected_mode == "real":
        return real_evidence_retriever()
    return InMemoryEvidenceRetriever()
