
from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_prediction_response_contract():
    response = client.post(
        "/api/predict",
        json={"url": "http://secure-paypa1.xyz/login"},
    )

    assert response.status_code == 200

    data = response.json()
    assert data["label"] in ["good", "bad"]
    assert 0 <= data["score"] <= 1
    assert data["threshold"] == 0.5
    assert "explanation" in data
    assert "red_flags" in data
    assert "disclaimer" in data


def test_prediction_is_deterministic():
    payload = {"url": "https://example.com/"}

    first = client.post("/api/predict", json=payload)
    second = client.post("/api/predict", json=payload)

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json() == second.json()


def test_invalid_urls_are_rejected():
    invalid_urls = [
        "",
        "   ",
        "example.com",
        "ftp://example.com",
    ]

    for url in invalid_urls:
        response = client.post("/api/predict", json={"url": url})
        assert response.status_code == 422, f"Unexpected result for {url!r}"


def test_missing_url_is_rejected():
    response = client.post("/api/predict", json={})

    assert response.status_code == 422
