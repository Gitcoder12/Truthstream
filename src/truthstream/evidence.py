"""Evidence retrieval abstractions and an in-memory MVP implementation."""

from collections.abc import Iterable
from typing import Protocol

from truthstream.models import Claim, Evidence, EvidenceStance, Source


class EvidenceRetriever(Protocol):
    """Retrieve evidence for a claim."""

    def retrieve(self, claim: Claim) -> list[Evidence]:
        """Return evidence related to the supplied claim."""


class InMemoryEvidenceRetriever:
    """Simple keyword-based evidence retriever for local demos and tests."""

    def __init__(self, evidence: Iterable[Evidence] | None = None) -> None:
        self._evidence = list(evidence or default_evidence())

    def retrieve(self, claim: Claim) -> list[Evidence]:
        claim_tokens = _tokens(claim.text)
        ranked = []
        for evidence in self._evidence:
            searchable = f"{evidence.title} {evidence.snippet} {evidence.source.name}"
            overlap = len(claim_tokens & _tokens(searchable))
            if overlap:
                ranked.append((overlap, evidence))
        ranked.sort(key=lambda item: item[0], reverse=True)
        return [evidence for _, evidence in ranked[:8]]


def default_evidence() -> list[Evidence]:
    """Seed evidence for the MVP demo dataset."""

    official = Source(name="Official Government Registry", credibility=0.95)
    newsroom = Source(name="Trusted News Wire", credibility=0.86)
    research = Source(name="Research Monitor", credibility=0.82)
    return [
        Evidence(
            source=official,
            title="No nationwide AI ban has been issued",
            snippet="The registry lists AI safety guidance but no blanket ban on AI systems.",
            stance=EvidenceStance.CONTRADICTS,
        ),
        Evidence(
            source=newsroom,
            title="Officials deny reports of an AI systems ban",
            snippet="Multiple agencies said current policy focuses on audits, not a ban.",
            stance=EvidenceStance.CONTRADICTS,
            recency_score=0.9,
        ),
        Evidence(
            source=research,
            title="Research publications on multilingual misinformation are rising",
            snippet="Recent papers report increased multilingual misinformation monitoring needs.",
            stance=EvidenceStance.SUPPORTS,
            recency_score=0.8,
        ),
    ]


def _tokens(text: str) -> set[str]:
    stopwords = {
        "the",
        "and",
        "has",
        "have",
        "was",
        "were",
        "with",
        "from",
        "that",
        "this",
        "but",
        "not",
    }
    return {
        token
        for token in "".join(ch.lower() if ch.isalnum() else " " for ch in text).split()
        if len(token) > 2 and token not in stopwords
    }
