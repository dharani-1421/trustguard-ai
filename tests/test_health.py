from fastapi.testclient import TestClient


def test_health_returns_ok(client: TestClient) -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["service"] == "trustguard-ai"
    assert "version" in payload
    assert "environment" in payload


def test_health_does_not_claim_ml_readiness(client: TestClient) -> None:
    """Health is process liveness only — no model or accuracy fields."""
    payload = client.get("/api/health").json()
    forbidden = {"accuracy", "precision", "recall", "f1", "confidence", "detection_rate"}
    assert forbidden.isdisjoint(payload.keys())
