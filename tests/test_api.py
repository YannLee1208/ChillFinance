"""API 测试。"""

from datetime import UTC, date, datetime
from decimal import Decimal
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from backend.app import create_app
from backend.domain.catalog import get_indicator
from backend.domain.models import Observation
from backend.storage.duckdb_store import DuckDBMacroStore


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


def test_unknown_observations_code_returns_404(
    temp_db_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("MACRO_DB_PATH", str(temp_db_path))
    client = TestClient(create_app())

    response = client.get("/api/observations/UNKNOWN")

    assert response.status_code == 404


def test_indicator_snapshot_returns_latest_and_previous(
    temp_db_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("MACRO_DB_PATH", str(temp_db_path))
    store = DuckDBMacroStore(temp_db_path)
    store.initialize()
    store.upsert_observations(
        [
            Observation(
                indicator_code="CN_GDP",
                period=date(2025, 9, 30),
                value=Decimal("4.8"),
                provider="world_bank",
                source=get_indicator("CN_GDP").source,
                ingested_at=datetime(2026, 5, 21, tzinfo=UTC),
            ),
            Observation(
                indicator_code="CN_GDP",
                period=date(2025, 12, 31),
                value=Decimal("5.0"),
                provider="world_bank",
                source=get_indicator("CN_GDP").source,
                ingested_at=datetime(2026, 5, 21, tzinfo=UTC),
            ),
        ]
    )
    client = TestClient(create_app())

    response = client.get("/api/indicators/CN_GDP")

    assert response.status_code == 200
    payload = response.json()
    assert payload["latest"]["period"] == "2025-12-31"
    assert payload["latest"]["value"] == "5.000000"
    assert payload["previous"]["period"] == "2025-09-30"
    assert payload["previous"]["value"] == "4.800000"
    assert len(payload["points"]) == 2


def test_latest_ingestion_run_returns_none_before_update(
    temp_db_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("MACRO_DB_PATH", str(temp_db_path))
    client = TestClient(create_app())

    response = client.get("/api/ingest/domains/rates/latest")

    assert response.status_code == 200
    assert response.json() is None
