"""公开煤炭价格数据适配器。"""

from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation
from typing import Any

import httpx

from backend.constant import COAL_PUBLIC_SERIES
from backend.domain.models import IndicatorDefinition, Observation


class CoalPublicProvider:
    """从 CCTD 与曹妃甸煤炭公开接口拉取煤炭价格。"""

    name = "coal_public"

    def __init__(self, timeout_seconds: int, user_agent: str) -> None:
        self.timeout_seconds = timeout_seconds
        self.user_agent = user_agent

    def supports(self, indicator: IndicatorDefinition) -> bool:
        """判断指标是否属于公开煤炭价格配置。"""

        return indicator.code in COAL_PUBLIC_SERIES

    async def fetch(self, indicator: IndicatorDefinition) -> list[Observation]:
        """按配置拉取并解析公开煤炭价格。"""

        config = COAL_PUBLIC_SERIES[indicator.code]
        payload = await self._fetch_payload(config["url"])
        source = str(config["source"])
        data_type = config["type"]
        if data_type == "cctd_price":
            return parse_cctd_price_payload(
                payload=payload,
                indicator_code=indicator.code,
                provider=self.name,
                source=source,
                value_field=str(config["value_field"]),
            )
        if data_type == "cfd_latest":
            return parse_cfd_latest_payload(
                payload=payload,
                indicator_code=indicator.code,
                provider=self.name,
                source=source,
                section=str(config["section"]),
                date_field=str(config["date_field"]),
                value_field=str(config["value_field"]),
            )
        if data_type == "cfd_history":
            return parse_cfd_history_payload(
                payload=payload,
                indicator_code=indicator.code,
                provider=self.name,
                source=source,
                date_list_key=str(config["date_list_key"]),
                value_list_key=str(config["value_list_key"]),
            )
        raise ValueError(f"Unsupported coal public series type: {data_type}")

    async def _fetch_payload(self, url: str) -> Any:
        headers = {
            "User-Agent": self.user_agent,
            "Referer": "https://www.cctd.com.cn/",
        }
        async with httpx.AsyncClient(
            timeout=self.timeout_seconds,
            headers=headers,
            verify=False,
            follow_redirects=True,
        ) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()


def parse_cctd_price_payload(
    *,
    payload: Any,
    indicator_code: str,
    provider: str,
    source: str,
    value_field: str,
) -> list[Observation]:
    """解析 CCTD Echarts JSON 价格序列。"""

    if not isinstance(payload, list):
        raise ValueError("CCTD price payload must be a list")

    ingested_at = datetime.now(UTC)
    observations: list[Observation] = []
    for item in payload:
        if not isinstance(item, dict):
            continue
        period_text = item.get("name")
        value_text = item.get(value_field)
        if _is_missing(period_text) or _is_missing(value_text):
            continue
        observations.append(
            Observation(
                indicator_code=indicator_code,
                period=datetime.strptime(str(period_text), "%Y-%m-%d").date(),
                value=_to_decimal(value_text),
                provider=provider,
                source=source,
                ingested_at=ingested_at,
            )
        )
    return sorted(observations, key=lambda observation: observation.period)


def parse_cfd_latest_payload(
    *,
    payload: Any,
    indicator_code: str,
    provider: str,
    source: str,
    section: str,
    date_field: str,
    value_field: str,
) -> list[Observation]:
    """解析曹妃甸煤贸数港当前价格字段。"""

    section_payload = _get_cfd_section(payload, section)
    period_text = section_payload.get(date_field)
    value_text = section_payload.get(value_field)
    if _is_missing(period_text) or _is_missing(value_text):
        return []

    ingested_at = datetime.now(UTC)
    return [
        Observation(
            indicator_code=indicator_code,
            period=datetime.strptime(str(period_text), "%Y-%m-%d").date(),
            value=_to_decimal(value_text),
            provider=provider,
            source=source,
            ingested_at=ingested_at,
        )
    ]


def parse_cfd_history_payload(
    *,
    payload: Any,
    indicator_code: str,
    provider: str,
    source: str,
    date_list_key: str,
    value_list_key: str,
) -> list[Observation]:
    """解析曹妃甸煤贸数港指数历史数组。"""

    data = _get_cfd_data(payload)
    date_values = data.get(date_list_key)
    price_values = data.get(value_list_key)
    if not isinstance(date_values, list) or not isinstance(price_values, list):
        raise ValueError("CFD history payload must contain date and value lists")

    ingested_at = datetime.now(UTC)
    observations: list[Observation] = []
    for period_text, value_text in zip(date_values, price_values, strict=False):
        if _is_missing(period_text) or _is_missing(value_text):
            continue
        observations.append(
            Observation(
                indicator_code=indicator_code,
                period=datetime.strptime(str(period_text), "%Y-%m-%d").date(),
                value=_to_decimal(value_text),
                provider=provider,
                source=source,
                ingested_at=ingested_at,
            )
        )
    return sorted(observations, key=lambda observation: observation.period)


def _get_cfd_data(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict) or not isinstance(payload.get("data"), dict):
        raise ValueError("CFD payload must contain a data object")
    return payload["data"]


def _get_cfd_section(payload: Any, section: str) -> dict[str, Any]:
    data = _get_cfd_data(payload)
    section_payload = data.get(section)
    if not isinstance(section_payload, dict):
        raise ValueError(f"CFD payload is missing section: {section}")
    return section_payload


def _is_missing(value: Any) -> bool:
    return value is None or str(value).strip() in {"", "--"}


def _to_decimal(value: Any) -> Decimal:
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"Invalid coal price value: {value}") from exc
