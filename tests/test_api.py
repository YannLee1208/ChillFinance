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


def test_indicator_snapshot_backfills_trade_derived_series_from_local_values(
    temp_db_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("MACRO_DB_PATH", str(temp_db_path))
    store = DuckDBMacroStore(temp_db_path)
    store.initialize()
    ingested_at = datetime(2026, 5, 21, tzinfo=UTC)
    store.upsert_observations(
        [
            Observation(
                indicator_code="CN_EXPORT_VALUE_USD",
                period=date(2026, 3, 1),
                value=Decimal("3200"),
                provider="akshare_china",
                source=get_indicator("CN_EXPORT_VALUE_USD").source,
                ingested_at=ingested_at,
            ),
            Observation(
                indicator_code="CN_EXPORT_VALUE_USD",
                period=date(2026, 4, 1),
                value=Decimal("3520"),
                provider="akshare_china",
                source=get_indicator("CN_EXPORT_VALUE_USD").source,
                ingested_at=ingested_at,
            ),
        ]
    )
    client = TestClient(create_app())

    response = client.get("/api/indicators/CN_EXPORT_MOM_USD")

    assert response.status_code == 200
    payload = response.json()
    assert payload["latest"]["period"] == "2026-04-01"
    assert Decimal(payload["latest"]["value"]) == Decimal("10.0")
    assert len(payload["points"]) == 1


def test_observations_backfills_trade_balance_from_local_values(
    temp_db_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("MACRO_DB_PATH", str(temp_db_path))
    store = DuckDBMacroStore(temp_db_path)
    store.initialize()
    ingested_at = datetime(2026, 5, 21, tzinfo=UTC)
    store.upsert_observations(
        [
            Observation(
                indicator_code="CN_EXPORT_VALUE_USD",
                period=date(2026, 4, 1),
                value=Decimal("3520"),
                provider="akshare_china",
                source=get_indicator("CN_EXPORT_VALUE_USD").source,
                ingested_at=ingested_at,
            ),
            Observation(
                indicator_code="CN_IMPORT_VALUE_USD",
                period=date(2026, 4, 1),
                value=Decimal("2740"),
                provider="akshare_china",
                source=get_indicator("CN_IMPORT_VALUE_USD").source,
                ingested_at=ingested_at,
            ),
        ]
    )
    client = TestClient(create_app())

    response = client.get("/api/observations/CN_TRADE_BALANCE_USD")

    assert response.status_code == 200
    payload = response.json()
    assert payload[0]["period"] == "2026-04-01"
    assert Decimal(payload[0]["value"]) == Decimal("780.0")


def test_latest_ingestion_run_returns_none_before_update(
    temp_db_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("MACRO_DB_PATH", str(temp_db_path))
    client = TestClient(create_app())

    response = client.get("/api/ingest/domains/rates/latest")

    assert response.status_code == 200
    assert response.json() is None
