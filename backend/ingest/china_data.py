"""ChinaData.live 数据源适配器。"""

from datetime import UTC, date, datetime
from decimal import Decimal, InvalidOperation
from typing import Any

import httpx

from backend.constant import CHINA_DATA_SERIES
from backend.domain.models import IndicatorDefinition, Observation


class ChinaDataProvider:
    """从 ChinaData.live 拉取公开中国宏观序列。"""

    name = "china_data"

    def __init__(self, timeout_seconds: int, user_agent: str) -> None:
        self.timeout_seconds = timeout_seconds
        self.user_agent = user_agent

    def supports(self, indicator: IndicatorDefinition) -> bool:
        """判断指标是否已经配置为 ChinaData.live 序列。"""

        return indicator.code in CHINA_DATA_SERIES

    async def fetch(self, indicator: IndicatorDefinition) -> list[Observation]:
        """拉取 JSON 并转换为观测值列表。"""

        dataset_id = CHINA_DATA_SERIES[indicator.code]
        url = f"https://chinadata.live/api/v2/data/{dataset_id}"
        headers = {"User-Agent": self.user_agent}

        async with httpx.AsyncClient(timeout=self.timeout_seconds, headers=headers) as client:
            response = await client.get(url)
            response.raise_for_status()

        return parse_china_data_payload(
            payload=response.json(),
            indicator_code=indicator.code,
            provider=self.name,
            source=indicator.source,
        )


def parse_china_data_payload(
    payload: Any,
    indicator_code: str,
    provider: str,
    source: str,
) -> list[Observation]:
    """解析 ChinaData.live API 返回值。"""

    if not isinstance(payload, dict) or payload.get("success") is not True:
        raise ValueError("ChinaData.live response is not successful")

    data_wrapper = payload.get("data")
    if not isinstance(data_wrapper, dict) or not isinstance(data_wrapper.get("data"), list):
        raise ValueError("ChinaData.live response must contain data.data list")

    ingested_at = datetime.now(UTC)
    observations: list[Observation] = []
    for item in data_wrapper["data"]:
        if not isinstance(item, dict):
            continue
        date_text = item.get("date")
        value = item.get("value")
        if not isinstance(date_text, str) or value in (None, ""):
            continue
        try:
            period = _parse_period(date_text)
            decimal_value = Decimal(str(value))
        except (InvalidOperation, ValueError) as exc:
            raise ValueError(f"Invalid ChinaData.live observation: {item}") from exc

        observations.append(
            Observation(
                indicator_code=indicator_code,
                period=period,
                value=decimal_value,
                provider=provider,
                source=source,
                ingested_at=ingested_at,
            )
        )

    return sorted(observations, key=lambda observation: observation.period)


def _parse_period(date_text: str) -> date:
    if len(date_text) == 7:
        return datetime.strptime(f"{date_text}-01", "%Y-%m-%d").date()
    return datetime.strptime(date_text, "%Y-%m-%d").date()
