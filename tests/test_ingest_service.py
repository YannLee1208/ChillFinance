"""采集服务测试。"""

from datetime import UTC, date, datetime
from decimal import Decimal

from backend.domain.models import IndicatorDefinition, Observation
from backend.ingest.service import IngestionService
from backend.storage.duckdb_store import DuckDBMacroStore


class DuplicateProvider:
    """返回重复日期数据的测试 provider。"""

    name = "duplicate"

    def supports(self, indicator: IndicatorDefinition) -> bool:
        """测试 provider 支持所有传入指标。"""

        return True

    async def fetch(self, indicator: IndicatorDefinition) -> list[Observation]:
        """返回同一天的重复观测值，模拟上游重复发布日期。"""

        first = Observation(
            indicator_code=indicator.code,
            period=date(2026, 1, 1),
            value=Decimal("1.23"),
            provider=self.name,
            source=indicator.source,
            ingested_at=datetime(2026, 1, 2, tzinfo=UTC),
        )
        second = first.model_copy(update={"value": Decimal("1.99")})
        return [first, second]


async def test_ingestion_service_dedupes_duplicate_observations(temp_db_path) -> None:
    store = DuckDBMacroStore(temp_db_path)
    store.initialize()
    indicator = IndicatorDefinition(
        code="DUPLICATE_SERIES",
        name="Duplicate series",
        domain="rates",
        region="Test",
        unit="%",
        frequency="daily",
        provider="duplicate",
        source="test",
        description="测试指标。",
    )
    service = IngestionService(store=store, providers=[DuplicateProvider()])

    result = await service.ingest([indicator])

    loaded = store.get_series(indicator.code)
    assert result.observation_count == 1
    assert result.failed_indicators == {}
    assert len(loaded) == 1
    assert loaded[0].value == Decimal("1.990000")
