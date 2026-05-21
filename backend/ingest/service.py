"""宏观数据采集服务。"""

from collections.abc import Iterable

from backend.domain.models import IndicatorDefinition
from backend.domain.providers import MacroDataProvider
from backend.storage.duckdb_store import DuckDBMacroStore


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
    ) -> int:
        """拉取并写入指标观测值，返回写入的观测值数量。"""

        indicator_list = list(indicators)
        self.store.upsert_indicators(indicator_list)

        total = 0
        for indicator in indicator_list:
            provider = self._select_provider(indicator, provider_name)
            if provider is None:
                continue

            observations = await provider.fetch(indicator)
            self.store.upsert_observations(observations)
            total += len(observations)

        return total

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
