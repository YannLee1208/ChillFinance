"""宏观数据采集服务。"""

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4

from backend.domain.models import IndicatorDefinition, IngestionAttemptRecord, IngestionRunRecord
from backend.domain.providers import MacroDataProvider
from backend.storage.duckdb_store import DuckDBMacroStore


@dataclass(frozen=True)
class IngestionResult:
    """一次采集的汇总结果。"""

    observation_count: int
    failed_indicators: dict[str, str]
    attempts: list[IngestionAttemptRecord]


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
        attempts: list[IngestionAttemptRecord] = []
        failures: dict[str, str] = {}
        for indicator in indicator_list:
            provider = self._select_provider(indicator, provider_name)
            if provider is None:
                continue

            started_at = datetime.now(UTC)
            try:
                observations = await provider.fetch(indicator)
            except Exception as exc:  # noqa: BLE001
                reason = f"{type(exc).__name__}: {exc}".strip()
                failures[indicator.code] = reason
                attempts.append(
                    IngestionAttemptRecord(
                        run_id="",
                        domain=indicator.domain,
                        indicator_code=indicator.code,
                        provider=provider.name,
                        status="failed",
                        message=f"{indicator.name} 更新失败：{reason}",
                        observation_count=0,
                        started_at=started_at,
                        finished_at=datetime.now(UTC),
                    )
                )
                continue
            if not observations:
                reason = "数据源可访问，但本次没有返回可写入的观测值。"
                failures[indicator.code] = reason
                attempts.append(
                    IngestionAttemptRecord(
                        run_id="",
                        domain=indicator.domain,
                        indicator_code=indicator.code,
                        provider=provider.name,
                        status="failed",
                        message=f"{indicator.name} 更新失败：{reason}",
                        observation_count=0,
                        started_at=started_at,
                        finished_at=datetime.now(UTC),
                    )
                )
                continue
            self.store.upsert_observations(observations)
            total += len(observations)
            attempts.append(
                IngestionAttemptRecord(
                    run_id="",
                    domain=indicator.domain,
                    indicator_code=indicator.code,
                    provider=provider.name,
                    status="success",
                    message=f"{indicator.name} 已更新，写入 {len(observations)} 条数据。",
                    observation_count=len(observations),
                    started_at=started_at,
                    finished_at=datetime.now(UTC),
                )
            )

        return IngestionResult(
            observation_count=total,
            failed_indicators=failures,
            attempts=attempts,
        )

    async def ingest_domain(
        self,
        domain: str,
        indicators: Iterable[IndicatorDefinition],
    ) -> IngestionRunRecord:
        """采集一个板块，并返回可展示的中文运行记录。"""

        run_id = uuid4().hex
        started_at = datetime.now(UTC)
        domain_indicators = [indicator for indicator in indicators if indicator.domain == domain]
        if not domain_indicators:
            finished_at = datetime.now(UTC)
            return IngestionRunRecord(
                run_id=run_id,
                domain=domain,
                status="failed",
                message="这个板块没有可更新的指标。",
                observation_count=0,
                success_count=0,
                failure_count=0,
                started_at=started_at,
                finished_at=finished_at,
            )

        result = await self.ingest(domain_indicators)
        finished_at = datetime.now(UTC)
        attempts = [
            attempt.model_copy(update={"run_id": run_id})
            for attempt in result.attempts
        ]
        success_count = sum(1 for attempt in attempts if attempt.status == "success")
        failure_count = sum(1 for attempt in attempts if attempt.status == "failed")
        status = "success" if failure_count == 0 else "partial" if success_count else "failed"
        message = (
            f"更新完成：成功 {success_count} 个指标，失败 {failure_count} 个指标，"
            f"写入 {result.observation_count} 条数据。"
        )

        run = IngestionRunRecord(
            run_id=run_id,
            domain=domain,
            status=status,
            message=message,
            observation_count=result.observation_count,
            success_count=success_count,
            failure_count=failure_count,
            started_at=started_at,
            finished_at=finished_at,
            attempts=attempts,
        )
        self.store.insert_ingestion_run(run)
        return run

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
