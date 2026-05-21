"""DuckDB 宏观数据存储。"""

from collections.abc import Iterable
from datetime import UTC, date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

import duckdb

from backend.domain.models import IndicatorDefinition, Observation


class DuckDBMacroStore:
    """使用 DuckDB 持久化宏观指标定义与观测值。"""

    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path

    def initialize(self) -> None:
        """创建数据库目录与基础表。"""

        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as connection:
            connection.execute(
                """
                create table if not exists indicators (
                    code varchar primary key,
                    name varchar not null,
                    domain varchar not null,
                    region varchar not null,
                    unit varchar not null,
                    frequency varchar not null,
                    provider varchar not null,
                    source varchar not null,
                    description varchar not null,
                    display_order integer not null
                )
                """
            )
            connection.execute(
                """
                create table if not exists observations (
                    indicator_code varchar not null,
                    period date not null,
                    value decimal(20, 6) not null,
                    provider varchar not null,
                    source varchar not null,
                    ingested_at timestamp not null,
                    primary key (indicator_code, period)
                )
                """
            )

    def upsert_indicators(self, definitions: Iterable[IndicatorDefinition]) -> None:
        """新增或替换指标定义，空输入不执行写入。"""

        rows: list[tuple[Any, ...]] = [
            (
                definition.code,
                definition.name,
                definition.domain,
                definition.region,
                definition.unit,
                definition.frequency,
                definition.provider,
                definition.source,
                definition.description,
                definition.display_order,
            )
            for definition in definitions
        ]
        if not rows:
            return

        with self._connect() as connection:
            self._executemany_in_transaction(
                connection,
                """
                insert or replace into indicators (
                    code,
                    name,
                    domain,
                    region,
                    unit,
                    frequency,
                    provider,
                    source,
                    description,
                    display_order
                )
                values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                rows,
            )

    def upsert_observations(self, observations: Iterable[Observation]) -> None:
        """新增或替换观测值，空输入不执行写入。"""

        rows: list[tuple[Any, ...]] = [
            (
                observation.indicator_code,
                observation.period,
                observation.value,
                observation.provider,
                observation.source,
                self._to_naive_utc(observation.ingested_at),
            )
            for observation in observations
        ]
        if not rows:
            return

        with self._connect() as connection:
            self._executemany_in_transaction(
                connection,
                """
                insert or replace into observations (
                    indicator_code,
                    period,
                    value,
                    provider,
                    source,
                    ingested_at
                )
                values (?, ?, ?, ?, ?, ?)
                """,
                rows,
            )

    def get_series(self, indicator_code: str, limit: int | None = None) -> list[Observation]:
        """按日期升序读取指定指标的观测序列。"""

        query = """
            select indicator_code, period, value, provider, source, ingested_at
            from observations
            where indicator_code = ?
            order by period asc
        """
        params: list[str | int] = [indicator_code]
        if limit is not None:
            query += " limit ?"
            params.append(limit)

        with self._connect() as connection:
            rows = connection.execute(query, params).fetchall()

        return [self._row_to_observation(row) for row in rows]

    def get_latest(self, indicator_code: str) -> Observation | None:
        """读取指定指标最新一期观测值。"""

        with self._connect() as connection:
            row = connection.execute(
                """
                select indicator_code, period, value, provider, source, ingested_at
                from observations
                where indicator_code = ?
                order by period desc
                limit 1
                """,
                [indicator_code],
            ).fetchone()

        if row is None:
            return None
        return self._row_to_observation(row)

    def _connect(self) -> duckdb.DuckDBPyConnection:
        return duckdb.connect(str(self.db_path))

    def _executemany_in_transaction(
        self,
        connection: duckdb.DuckDBPyConnection,
        query: str,
        rows: list[tuple[Any, ...]],
    ) -> None:
        connection.execute("begin transaction")
        try:
            connection.executemany(query, rows)
            connection.execute("commit")
        except Exception:
            connection.execute("rollback")
            raise

    def _to_naive_utc(self, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            return value
        return value.astimezone(UTC).replace(tzinfo=None)

    def _row_to_observation(self, row: tuple[Any, ...]) -> Observation:
        indicator_code, period, value, provider, source, ingested_at = row
        return Observation(
            indicator_code=indicator_code,
            period=period if isinstance(period, date) else date.fromisoformat(period),
            value=value if isinstance(value, Decimal) else Decimal(str(value)),
            provider=provider,
            source=source,
            ingested_at=(
                ingested_at
                if isinstance(ingested_at, datetime)
                else datetime.fromisoformat(ingested_at)
            ),
        )
