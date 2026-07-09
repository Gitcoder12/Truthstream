import pytest

pytest.importorskip("fastapi")


def test_health_endpoint() -> None:
    from fastapi.testclient import TestClient

    from truthstream.api import app

    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_verify_endpoint() -> None:
    from fastapi.testclient import TestClient

    from truthstream.api import app

    client = TestClient(app)
    response = client.post("/verify", json={"text": "Country X has banned AI systems."})

    assert response.status_code == 200
    body = response.json()
    assert body[0]["claim"]["text"] == "Country X has banned AI systems."
    assert body[0]["status"] == "likely_false"
    assert body[0]["evidence_summary"]["contradicting_count"] == 2


def test_verify_endpoint_rejects_empty_text() -> None:
    from fastapi.testclient import TestClient

    from truthstream.api import app

    client = TestClient(app)
    response = client.post("/verify", json={"text": "   "})

    assert response.status_code == 400


def test_verify_batch_endpoint_preserves_order() -> None:
    from fastapi.testclient import TestClient

    from truthstream.api import app

    client = TestClient(app)
    response = client.post(
        "/verify/batch",
        json=[
            {"text": "Country X has banned AI systems."},
            {"text": "The moon has a new public library."},
        ],
    )

    assert response.status_code == 200
    body = response.json()
    assert body[0][0]["status"] == "likely_false"
    assert body[1][0]["status"] == "insufficient_evidence"
