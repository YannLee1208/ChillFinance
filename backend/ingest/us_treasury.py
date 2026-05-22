"""美国财政部每日国债收益率数据源。"""

import csv
from collections.abc import Iterable
from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation
from io import StringIO

import httpx

from backend.constant import US_TREASURY_BACKFILL_START_YEAR, US_TREASURY_SERIES
from backend.domain.models import IndicatorDefinition, Observation


class USTreasuryProvider:
    """从美国财政部官方 CSV 拉取每日国债收益率曲线。"""

    name = "us_treasury"

    def __init__(self, timeout_seconds: int, user_agent: str) -> None:
        self.timeout_seconds = timeout_seconds
        self.user_agent = user_agent
        self._cache: dict[str, list[dict[str, str]]] = {}

    def supports(self, indicator: IndicatorDefinition) -> bool:
        """判断指标是否属于美国财政部国债收益率。"""

        return indicator.code in US_TREASURY_SERIES

    async def fetch(self, indicator: IndicatorDefinition) -> list[Observation]:
        """拉取 2020 年以来的月度 CSV，并抽取对应期限列。"""

        rows = await self._fetch_recent_rows()
        column = US_TREASURY_SERIES[indicator.code]
        ingested_at = datetime.now(UTC)
        observations: list[Observation] = []
        for row in rows:
            value_text = row.get(column, "").strip()
            date_text = row.get("Date", "").strip()
            if value_text in {"", "N/A"} or not date_text:
                continue
            try:
                period = datetime.strptime(date_text, "%m/%d/%Y").date()
                value = Decimal(value_text)
            except (InvalidOperation, ValueError) as exc:
                raise ValueError(f"Invalid U.S. Treasury observation: {row}") from exc
            observations.append(
                Observation(
                    indicator_code=indicator.code,
                    period=period,
                    value=value,
                    provider=self.name,
                    source=indicator.source,
                    ingested_at=ingested_at,
                )
            )
        return sorted(observations, key=lambda observation: observation.period)

    async def _fetch_recent_rows(self) -> list[dict[str, str]]:
        # 财政部按月份提供 CSV；从 2020 年回填，覆盖完整监控窗口。
        months = list(_month_codes_since(start_year=US_TREASURY_BACKFILL_START_YEAR))
        missing_months = [month for month in months if month not in self._cache]
        if missing_months:
            headers = {"User-Agent": self.user_agent}
            async with httpx.AsyncClient(timeout=self.timeout_seconds, headers=headers) as client:
                for month in missing_months:
                    response = await client.get(_month_csv_url(month))
                    response.raise_for_status()
                    self._cache[month] = parse_us_treasury_csv(response.text)

        rows: list[dict[str, str]] = []
        for month in months:
            rows.extend(self._cache.get(month, []))
        unique_rows = {row["Date"]: row for row in rows if row.get("Date")}
        return sorted(unique_rows.values(), key=lambda row: row["Date"])


def parse_us_treasury_csv(csv_text: str) -> list[dict[str, str]]:
    """解析美国财政部国债收益率 CSV。"""

    reader = csv.DictReader(StringIO(csv_text))
    return [row for row in reader if row.get("Date")]


def _recent_month_codes(month_count: int) -> Iterable[str]:
    today = datetime.now(UTC).date()
    year = today.year
    month = today.month
    for _ in range(month_count):
        yield f"{year}{month:02d}"
        month -= 1
        if month == 0:
            month = 12
            year -= 1


def _month_codes_since(start_year: int) -> Iterable[str]:
    """生成 start_year 年初至当前月的财政部月度 CSV 编码。"""

    today = datetime.now(UTC).date()
    year = start_year
    month = 1
    while (year, month) <= (today.year, today.month):
        yield f"{year}{month:02d}"
        month += 1
        if month == 13:
            month = 1
            year += 1


def _month_csv_url(month_code: str) -> str:
    base = (
        "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/"
        f"daily-treasury-rates.csv/all/{month_code}"
    )
    return (
        f"{base}?type=daily_treasury_yield_curve"
        f"&field_tdr_date_value_month={month_code}&page&_format=csv"
    )
