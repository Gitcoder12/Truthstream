from truthstream.provenance import is_source_backed_evidence, provenance_summary


def record(url="https://example.org/report", evidence_id="ev-1",
           retrieved_at="2026-11-20T08:00:00Z"):
    return {
        "evidence_id": evidence_id,
        "retrieved_at": retrieved_at,
        "source": {"name": "Example source", "url": url, "credibility": 0.9},
    }


def test_requires_https_url_stable_id_and_timestamp():
    assert is_source_backed_evidence(record())
    assert not is_source_backed_evidence(record(url=None))
    assert not is_source_backed_evidence(record(url="http://example.org"))
    assert not is_source_backed_evidence(record(evidence_id=""))
    assert not is_source_backed_evidence(record(retrieved_at="yesterday"))


def test_demo_placeholder_is_not_source_backed():
    summary = provenance_summary({
        "supporting_evidence": [],
        "contradicting_evidence": [record(url=None)],
        "neutral_evidence": [],
    })
    assert summary["status"] == "demo_or_incomplete"
    assert summary["verified_items"] == 0


def test_source_backed_requires_every_item_to_have_provenance():
    summary = provenance_summary({
        "supporting_evidence": [record()],
        "contradicting_evidence": [record(evidence_id="ev-2")],
        "neutral_evidence": [],
    })
    assert summary["status"] == "source_backed"
    assert summary["source_count"] == 1
    assert summary["evidence_count"] == 2


def test_empty_evidence_is_not_a_verified_claim():
    assert provenance_summary({})["status"] == "no_evidence"
