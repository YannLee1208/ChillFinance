"""DuckDB 存储测试。"""

from datetime import UTC, date, datetime
from decimal import Decimal

from backend.domain.models import IndicatorDefinition, Observation
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
