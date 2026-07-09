from truthstream.evidence import CompositeEvidenceRetriever
from truthstream.models import Claim, Evidence, EvidenceStance, Source
from truthstream.providers import (
    CachedEvidenceProvider,
    CrossrefEvidenceProvider,
    OpenAlexEvidenceProvider,
    ProviderConfig,
    WikipediaEvidenceProvider,
)


def test_wikipedia_provider_maps_search_results_to_neutral_evidence() -> None:
    def opener(url: str, headers: dict[str, str], timeout: float) -> dict[str, object]:
        assert "wikipedia" in url
        assert headers["User-Agent"].startswith("TruthStream")
        assert timeout == 1
        return {"pages": [{"title": "Example", "key": "Example", "excerpt": "Result"}]}

    provider = WikipediaEvidenceProvider(ProviderConfig(timeout_seconds=1), opener=opener)

    evidence = provider.fetch(Claim(text="example claim"))

    assert evidence[0].source.name == "Wikipedia"
    assert evidence[0].stance == EvidenceStance.NEUTRAL
    assert evidence[0].title == "Example"


def test_crossref_provider_maps_work_metadata() -> None:
    def opener(url: str, headers: dict[str, str], timeout: float) -> dict[str, object]:
        return {
            "message": {
                "items": [
                    {
                        "title": ["Research result"],
                        "container-title": ["Journal"],
                        "URL": "https://doi.org/10.0000/example",
                    }
                ]
            }
        }

    evidence = CrossrefEvidenceProvider(opener=opener).fetch(Claim(text="research claim"))

    assert evidence[0].source.name == "Crossref"
    assert evidence[0].title == "Research result"
    assert evidence[0].snippet == "Journal"


def test_openalex_provider_maps_work_metadata() -> None:
    def opener(url: str, headers: dict[str, str], timeout: float) -> dict[str, object]:
        return {
            "results": [
                {
                    "display_name": "Open research result",
                    "id": "https://openalex.org/W1",
                    "publication_year": 2026,
                    "primary_location": {"source": {"display_name": "Archive"}},
                }
            ]
        }

    evidence = OpenAlexEvidenceProvider(opener=opener).fetch(Claim(text="research claim"))

    assert evidence[0].source.name == "OpenAlex"
    assert evidence[0].title == "Open research result"
    assert evidence[0].snippet == "2026 | Archive"


def test_cached_provider_reuses_claim_response() -> None:
    calls = 0

    class Provider:
        name = "fake"

        def fetch(self, claim: Claim) -> list[Evidence]:
            nonlocal calls
            calls += 1
            return [
                Evidence(
                    source=Source(name="Fake", credibility=0.5),
                    title=claim.text,
                    snippet="Cached",
                    stance=EvidenceStance.NEUTRAL,
                )
            ]

    provider = CachedEvidenceProvider(Provider())

    assert provider.fetch(Claim(text="Same claim"))[0].title == "Same claim"
    assert provider.fetch(Claim(text="Same claim"))[0].title == "Same claim"
    assert calls == 1


def test_composite_retriever_keeps_working_when_provider_fails() -> None:
    class BrokenProvider:
        name = "broken"

        def fetch(self, claim: Claim) -> list[Evidence]:
            raise RuntimeError("provider down")

    class WorkingProvider:
        name = "working"

        def fetch(self, claim: Claim) -> list[Evidence]:
            return [
                Evidence(
                    source=Source(name="Working", credibility=0.8),
                    title="Result",
                    snippet="Result",
                    stance=EvidenceStance.NEUTRAL,
                )
            ]

    evidence = CompositeEvidenceRetriever([BrokenProvider(), WorkingProvider()]).retrieve(
        Claim(text="claim")
    )

    assert len(evidence) == 1
    assert evidence[0].source.name == "Working"
