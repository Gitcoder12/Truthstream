"""Confidence scoring for evidence-centered verification."""

from truthstream.models import Evidence, EvidenceStance, EvidenceSummary, VerificationStatus


def score_evidence(
    evidence: list[Evidence],
) -> tuple[float, VerificationStatus, str, EvidenceSummary]:
    """Calculate a normalized confidence score, status, explanation, and evidence summary."""

    supporting = [item for item in evidence if item.stance == EvidenceStance.SUPPORTS]
    contradicting = [item for item in evidence if item.stance == EvidenceStance.CONTRADICTS]
    neutral = [item for item in evidence if item.stance == EvidenceStance.NEUTRAL]

    support_weight = _weight(supporting)
    contradiction_weight = _weight(contradicting)
    summary = EvidenceSummary(
        supporting_count=len(supporting),
        contradicting_count=len(contradicting),
        neutral_count=len(neutral),
        supporting_weight=round(support_weight, 4),
        contradicting_weight=round(contradiction_weight, 4),
    )
    total = support_weight + contradiction_weight

    if total == 0:
        return (
            0.5,
            VerificationStatus.INSUFFICIENT_EVIDENCE,
            "No supporting or contradicting evidence was found in the configured sources.",
            summary,
        )

    confidence = support_weight / total
    status = _status(confidence, len(supporting), len(contradicting))
    explanation = _explain(confidence, supporting, contradicting)
    return confidence, status, explanation, summary


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
    strongest_stance = "supporting" if confidence >= 0.5 else "contradicting"
    return (
        f"Confidence is {confidence:.0%} with stronger {strongest_stance} evidence, based on "
        f"{len(supporting)} supporting item(s) from {len(support_sources)} source(s) and "
        f"{len(contradicting)} contradicting item(s) from "
        f"{len(contradiction_sources)} source(s)."
    )
