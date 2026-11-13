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


def test_verify_endpoint_rejects_missing_text() -> None:
    from fastapi.testclient import TestClient

    from truthstream.api import app

    response = TestClient(app).post("/verify", json={"source": "test"})

    assert response.status_code == 422


def test_verify_endpoint_rejects_blank_text() -> None:
    from fastapi.testclient import TestClient

    from truthstream.api import app

    response = TestClient(app).post("/verify", json={"text": "   "})

    assert response.status_code == 422
