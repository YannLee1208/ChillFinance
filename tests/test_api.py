"""API 测试。"""

from fastapi.testclient import TestClient

from backend.app import create_app


def test_health_endpoint() -> None:
    client = TestClient(create_app())

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_catalog_endpoint_contains_rates() -> None:
    client = TestClient(create_app())

    response = client.get("/api/catalog")

    assert response.status_code == 200
    payload = response.json()
    assert any(item["domain"] == "rates" for item in payload)
