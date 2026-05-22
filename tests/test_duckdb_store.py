"""DuckDB 存储测试。"""

from datetime import UTC, date, datetime, timedelta, timezone
from decimal import Decimal

import pytest
from duckdb import ConversionException

from backend.domain.models import (
    IndicatorDefinition,
    IngestionAttemptRecord,
    IngestionRunRecord,
    Observation,
)
from backend.storage.duckdb_store import DuckDBMacroStore


def test_store_upserts_and_reads_observations(temp_db_path) -> None:
    store = DuckDBMacroStore(temp_db_path)
    store.initialize()
    definition = IndicatorDefinition(
        code="TEST_SERIES",
        name="Test series",
        domain="rates",
        region="Test",
        unit="%",
        frequency="daily",
        provider="test",
        source="test",
        description="测试指标。",
    )
    observations = [
        Observation(
            indicator_code="TEST_SERIES",
            period=date(2026, 1, 1),
            value=Decimal("1.23"),
            provider="test",
            source="test",
            ingested_at=datetime(2026, 1, 2, tzinfo=UTC),
        ),
        Observation(
            indicator_code="TEST_SERIES",
            period=date(2026, 1, 2),
            value=Decimal("1.25"),
            provider="test",
            source="test",
            ingested_at=datetime(2026, 1, 3, tzinfo=UTC),
        ),
    ]

    store.upsert_indicators([definition])
    store.upsert_observations(observations)

    loaded = store.get_series("TEST_SERIES")
    latest = store.get_latest("TEST_SERIES")

    assert [item.value for item in loaded] == [Decimal("1.230000"), Decimal("1.250000")]
    assert latest is not None
    assert latest.period == date(2026, 1, 2)


def test_store_replaces_same_indicator_period(temp_db_path) -> None:
    store = DuckDBMacroStore(temp_db_path)
    store.initialize()
    first = Observation(
        indicator_code="TEST_SERIES",
        period=date(2026, 1, 1),
        value=Decimal("1.23"),
        provider="test",
        source="test",
        ingested_at=datetime(2026, 1, 2, tzinfo=UTC),
    )
    second = first.model_copy(update={"value": Decimal("1.99")})

    store.upsert_observations([first])
    store.upsert_observations([second])

    loaded = store.get_series("TEST_SERIES")

    assert len(loaded) == 1
    assert loaded[0].value == Decimal("1.990000")


def test_store_rolls_back_observation_batch_when_later_row_fails(temp_db_path) -> None:
    store = DuckDBMacroStore(temp_db_path)
    store.initialize()
    observations = [
        Observation(
            indicator_code="ATOMIC_SERIES",
            period=date(2026, 1, 1),
            value=Decimal("1.23"),
            provider="test",
            source="test",
            ingested_at=datetime(2026, 1, 2, tzinfo=UTC),
        ),
        Observation(
            indicator_code="ATOMIC_SERIES",
            period=date(2026, 1, 2),
            value=Decimal("123456789012345.123456"),
            provider="test",
            source="test",
            ingested_at=datetime(2026, 1, 3, tzinfo=UTC),
        ),
    ]

    with pytest.raises(ConversionException):
        store.upsert_observations(observations)

    assert store.get_series("ATOMIC_SERIES") == []


def test_store_normalizes_aware_timestamps_to_naive_utc(temp_db_path) -> None:
    store = DuckDBMacroStore(temp_db_path)
    store.initialize()
    observation = Observation(
        indicator_code="TZ_SERIES",
        period=date(2026, 1, 1),
        value=Decimal("1.23"),
        provider="test",
        source="test",
        ingested_at=datetime(
            2026,
            1,
            2,
            8,
            30,
            tzinfo=timezone(timedelta(hours=8)),
        ),
    )

    store.upsert_observations([observation])

    loaded = store.get_latest("TZ_SERIES")

    assert loaded is not None
    assert loaded.ingested_at == datetime(2026, 1, 2, 0, 30)


def test_store_persists_latest_ingestion_run(temp_db_path) -> None:
    store = DuckDBMacroStore(temp_db_path)
    store.initialize()
    started_at = datetime(2026, 1, 2, 8, 30, tzinfo=UTC)
    finished_at = datetime(2026, 1, 2, 8, 31, tzinfo=UTC)
    run = IngestionRunRecord(
        run_id="run-1",
        domain="rates",
        status="partial",
        message="更新完成：成功 1 个指标，失败 1 个指标，写入 10 条数据。",
        observation_count=10,
        success_count=1,
        failure_count=1,
        started_at=started_at,
        finished_at=finished_at,
        attempts=[
            IngestionAttemptRecord(
                run_id="run-1",
                domain="rates",
                indicator_code="US_DGS10",
                provider="fred",
                status="success",
                message="U.S. Treasury 10Y yield 已更新，写入 10 条数据。",
                observation_count=10,
                started_at=started_at,
                finished_at=finished_at,
            )
        ],
    )

    store.insert_ingestion_run(run)

    loaded = store.get_latest_ingestion_run("rates")

    assert loaded is not None
    assert loaded.run_id == "run-1"
    assert loaded.status == "partial"
    assert loaded.attempts[0].indicator_code == "US_DGS10"
    assert loaded.attempts[0].observation_count == 10
