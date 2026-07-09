"""Composable verification pipeline for TruthStream."""

from truthstream.evidence import EvidenceRetriever, InMemoryEvidenceRetriever
from truthstream.extraction import ClaimExtractor
from truthstream.models import EvidenceStance, StreamItem, VerificationResult
from truthstream.scoring import score_evidence


class VerificationPipeline:
    """Extract claims, retrieve evidence, score confidence, and explain results."""

    def __init__(
        self,
        extractor: ClaimExtractor | None = None,
        retriever: EvidenceRetriever | None = None,
    ) -> None:
        self.extractor = extractor or ClaimExtractor()
        self.retriever = retriever or InMemoryEvidenceRetriever()

    def verify(self, item: StreamItem) -> list[VerificationResult]:
        results: list[VerificationResult] = []
        for claim in self.extractor.extract(item):
            evidence = self.retriever.retrieve(claim)
            confidence, status, explanation = score_evidence(evidence)
            results.append(
                VerificationResult(
                    claim=claim,
                    confidence_score=round(confidence, 4),
                    status=status,
                    supporting_evidence=[
                        item for item in evidence if item.stance == EvidenceStance.SUPPORTS
                    ],
                    contradicting_evidence=[
                        item for item in evidence if item.stance == EvidenceStance.CONTRADICTS
                    ],
                    neutral_evidence=[
                        item for item in evidence if item.stance == EvidenceStance.NEUTRAL
                    ],
                    explanation=explanation,
                )
            )
        return results
