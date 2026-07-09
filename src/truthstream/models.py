"""Domain models for TruthStream's evidence-centered verification pipeline."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum


class EvidenceStance(StrEnum):
    """How a piece of evidence relates to a claim."""

    SUPPORTS = "supports"
    CONTRADICTS = "contradicts"
    NEUTRAL = "neutral"


class VerificationStatus(StrEnum):
    """Human-readable confidence band for a verification result."""

    LIKELY_TRUE = "likely_true"
    MIXED = "mixed"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    LIKELY_FALSE = "likely_false"


@dataclass(slots=True)
class Source:
    """Metadata for a source used during evidence retrieval."""

    name: str
    url: str | None = None
    credibility: float = 1.0

    def __post_init__(self) -> None:
        _validate_range("credibility", self.credibility)


@dataclass(slots=True)
class Evidence:
    """Evidence found for or against a claim."""

    source: Source
    title: str
    snippet: str
    stance: EvidenceStance
    recency_score: float = 1.0

    def __post_init__(self) -> None:
        self.stance = EvidenceStance(self.stance)
        _validate_range("recency_score", self.recency_score)


@dataclass(slots=True)
class Claim:
    """A factual claim extracted from an incoming text item."""

    text: str
    entities: list[str] = field(default_factory=list)


@dataclass(slots=True)
class StreamItem:
    """Incoming content to verify."""

    text: str
    source: str | None = None

    def __post_init__(self) -> None:
        if not self.text.strip():
            raise ValueError("StreamItem.text must not be empty")


@dataclass(slots=True)
class EvidenceSummary:
    """Aggregated evidence counts and weights for a verification result."""

    supporting_count: int
    contradicting_count: int
    neutral_count: int
    supporting_weight: float
    contradicting_weight: float


@dataclass(slots=True)
class VerificationResult:
    """Transparent verification output for a single claim."""

    claim: Claim
    confidence_score: float
    status: VerificationStatus
    supporting_evidence: list[Evidence]
    contradicting_evidence: list[Evidence]
    neutral_evidence: list[Evidence]
    explanation: str
    evidence_summary: EvidenceSummary

    def __post_init__(self) -> None:
        self.status = VerificationStatus(self.status)
        _validate_range("confidence_score", self.confidence_score)

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable representation."""

        return asdict(self)


def _validate_range(field_name: str, value: float) -> None:
    if not 0 <= value <= 1:
        raise ValueError(f"{field_name} must be between 0 and 1")
