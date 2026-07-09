"""Evidence retrieval abstractions and an in-memory MVP implementation."""

from collections.abc import Iterable
from typing import Protocol

from truthstream.models import Claim, Evidence, EvidenceStance, Source
from truthstream.providers import EvidenceProvider, default_providers


class EvidenceRetriever(Protocol):
    """Retrieve evidence for a claim."""

    def retrieve(self, claim: Claim) -> list[Evidence]:
        """Return evidence related to the supplied claim."""


class CompositeEvidenceRetriever:
    """Retrieve evidence from multiple providers while tolerating provider failures."""

    def __init__(self, providers: Iterable[EvidenceProvider], max_results: int = 12) -> None:
        self._providers = list(providers)
        self._max_results = max_results

    def retrieve(self, claim: Claim) -> list[Evidence]:
        evidence: list[Evidence] = []
        for provider in self._providers:
            try:
                evidence.extend(provider.fetch(claim))
            except Exception:
                continue
        return evidence[: self._max_results]


class InMemoryEvidenceRetriever:
    """Simple keyword-based evidence retriever for local demos and tests."""

    def __init__(
        self, evidence: Iterable[Evidence] | None = None, min_overlap: int = 2
    ) -> None:
        self._evidence = list(evidence or default_evidence())
        self._min_overlap = min_overlap

    def retrieve(self, claim: Claim) -> list[Evidence]:
        claim_tokens = _tokens(claim.text)
        ranked = []
        for evidence in self._evidence:
            searchable = f"{evidence.title} {evidence.snippet} {evidence.source.name}"
            overlap = len(claim_tokens & _tokens(searchable))
            if overlap >= self._min_overlap:
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
        "new",
        "public",
    }
    return {
        _stem(token)
        for token in "".join(ch.lower() if ch.isalnum() else " " for ch in text).split()
        if len(token) > 2 and token not in stopwords
    }


def _stem(token: str) -> str:
    """Apply tiny deterministic normalization for the MVP retriever."""

    if token.endswith("ies") and len(token) > 4:
        return f"{token[:-3]}y"
    if token.endswith("ed") and len(token) > 4:
        stem = token[:-2]
        if len(stem) > 2 and stem[-1] == stem[-2]:
            return stem[:-1]
        return stem
    if token.endswith("s") and len(token) > 4:
        return token[:-1]
    return token


def real_evidence_retriever(max_results: int = 12) -> CompositeEvidenceRetriever:
    """Build a retriever using the default real evidence providers.

    This factory keeps the default pipeline backward compatible: existing callers still get the
    deterministic in-memory retriever unless they explicitly opt into remote providers.
    """

    return CompositeEvidenceRetriever(default_providers(), max_results=max_results)
