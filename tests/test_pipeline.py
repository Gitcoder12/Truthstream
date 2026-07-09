from truthstream.models import StreamItem, VerificationStatus
from truthstream.pipeline import VerificationPipeline


def test_pipeline_contradicts_unsupported_ai_ban_claim() -> None:
    results = VerificationPipeline().verify(StreamItem(text="Country X has banned AI systems."))

    assert len(results) == 1
    assert results[0].status == VerificationStatus.LIKELY_FALSE
    assert results[0].confidence_score == 0
    assert results[0].evidence_summary.contradicting_count == 2
    assert results[0].evidence_summary.supporting_count == 0


def test_pipeline_reports_insufficient_evidence_for_unknown_claim() -> None:
    results = VerificationPipeline().verify(StreamItem(text="The moon has a new public library."))

    assert len(results) == 1
    assert results[0].status == VerificationStatus.INSUFFICIENT_EVIDENCE
    assert results[0].confidence_score == 0.5
    assert results[0].evidence_summary.supporting_weight == 0
    assert results[0].evidence_summary.contradicting_weight == 0
