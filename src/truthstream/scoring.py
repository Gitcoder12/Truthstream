"""Confidence scoring for evidence-centered verification."""

from truthstream.models import Evidence, EvidenceStance, VerificationStatus


def score_evidence(evidence: list[Evidence]) -> tuple[float, VerificationStatus, str]:
    """Calculate a normalized confidence score and explanation."""

    supporting = [item for item in evidence if item.stance == EvidenceStance.SUPPORTS]
    contradicting = [item for item in evidence if item.stance == EvidenceStance.CONTRADICTS]

    support_weight = _weight(supporting)
    contradiction_weight = _weight(contradicting)
    total = support_weight + contradiction_weight

    if total == 0:
        return (
            0.5,
            VerificationStatus.INSUFFICIENT_EVIDENCE,
            "No supporting or contradicting evidence was found in the configured sources.",
        )

    confidence = support_weight / total
    status = _status(confidence, len(supporting), len(contradicting))
    explanation = _explain(confidence, supporting, contradicting)
    return confidence, status, explanation


def _weight(evidence: list[Evidence]) -> float:
    return sum(item.source.credibility * item.recency_score for item in evidence)


def _status(
    confidence: float, supporting_count: int, contradicting_count: int
) -> VerificationStatus:
    if supporting_count == 0 and contradicting_count > 0:
        return VerificationStatus.LIKELY_FALSE
    if contradicting_count == 0 and supporting_count > 0:
        return VerificationStatus.LIKELY_TRUE
    if confidence >= 0.7:
        return VerificationStatus.LIKELY_TRUE
    if confidence <= 0.3:
        return VerificationStatus.LIKELY_FALSE
    return VerificationStatus.MIXED


def _explain(confidence: float, supporting: list[Evidence], contradicting: list[Evidence]) -> str:
    support_sources = {item.source.name for item in supporting}
    contradiction_sources = {item.source.name for item in contradicting}
    return (
        f"Confidence is {confidence:.0%} based on {len(supporting)} supporting item(s) "
        f"from {len(support_sources)} source(s) and {len(contradicting)} contradicting item(s) "
        f"from {len(contradiction_sources)} source(s)."
    )
