"""World Bank 宏观数据适配器。"""

from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation
from typing import Any

import httpx

from backend.constant import WORLD_BANK_SERIES
from backend.domain.models import IndicatorDefinition, Observation


class WorldBankProvider:
    """从 World Bank Indicators API 拉取年度宏观序列。"""

    name = "world_bank"

    def __init__(self, timeout_seconds: int, user_agent: str) -> None:
        self.timeout_seconds = timeout_seconds
        self.user_agent = user_agent

    def supports(self, indicator: IndicatorDefinition) -> bool:
        """判断指标是否属于已配置的 World Bank 序列。"""

        return indicator.code in WORLD_BANK_SERIES

    async def fetch(self, indicator: IndicatorDefinition) -> list[Observation]:
        """拉取 World Bank JSON 并转换为观测值列表。"""

        country_code, series_code = WORLD_BANK_SERIES[indicator.code]
        url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/{series_code}"
        params = {"format": "json", "per_page": 20000}
        headers = {"User-Agent": self.user_agent}

        async with httpx.AsyncClient(timeout=self.timeout_seconds, headers=headers) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()

        return parse_world_bank_payload(
            payload=response.json(),
            indicator_code=indicator.code,
            provider=self.name,
            source=indicator.source,
        )


def parse_world_bank_payload(
    payload: Any,
    indicator_code: str,
    provider: str,
    source: str,
) -> list[Observation]:
    """解析 World Bank API 返回值。"""

    if not isinstance(payload, list) or len(payload) < 2 or not isinstance(payload[1], list):
        raise ValueError("World Bank response must be a two-item list")

    ingested_at = datetime.now(UTC)
    observations: list[Observation] = []
    for item in payload[1]:
        if not isinstance(item, dict):
            continue
        value = item.get("value")
        year = item.get("date")
        if value in (None, "") or year in (None, ""):
            continue
        try:
            decimal_value = Decimal(str(value))
            period_year = int(str(year))
        except (InvalidOperation, ValueError) as exc:
            raise ValueError(f"Invalid World Bank observation: {item}") from exc

        observations.append(
            Observation(
                indicator_code=indicator_code,
                period=datetime(period_year, 12, 31, tzinfo=UTC).date(),
                value=decimal_value,
                provider=provider,
                source=source,
                ingested_at=ingested_at,
            )
        )

    return sorted(observations, key=lambda observation: observation.period)
