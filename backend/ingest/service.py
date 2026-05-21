"""宏观数据采集服务。"""

from collections.abc import Iterable
from dataclasses import dataclass

from backend.domain.models import IndicatorDefinition
from backend.domain.providers import MacroDataProvider
from backend.storage.duckdb_store import DuckDBMacroStore


@dataclass(frozen=True)
class IngestionResult:
    """一次采集的汇总结果。"""

    observation_count: int
    failed_indicators: dict[str, str]


class IngestionService:
    """协调指标目录、数据源适配器与持久化存储。"""

    def __init__(
        self,
        store: DuckDBMacroStore,
        providers: Iterable[MacroDataProvider],
    ) -> None:
        self.store = store
        self.providers = list(providers)

    async def ingest(
        self,
        indicators: Iterable[IndicatorDefinition],
        provider_name: str | None = None,
    ) -> IngestionResult:
        """拉取并写入指标观测值，返回写入的观测值数量。"""

        indicator_list = list(indicators)
        self.store.upsert_indicators(indicator_list)

        total = 0
        failures: dict[str, str] = {}
        for indicator in indicator_list:
            provider = self._select_provider(indicator, provider_name)
            if provider is None:
                continue

            try:
                observations = await provider.fetch(indicator)
            except Exception as exc:  # noqa: BLE001
                failures[indicator.code] = f"{type(exc).__name__}: {exc}"
                continue
            self.store.upsert_observations(observations)
            total += len(observations)

        return IngestionResult(observation_count=total, failed_indicators=failures)

    def _select_provider(
        self,
        indicator: IndicatorDefinition,
        provider_name: str | None = None,
    ) -> MacroDataProvider | None:
        for provider in self.providers:
            if provider_name is not None and provider.name != provider_name:
                continue
            if provider.supports(indicator):
                return provider
        return None
