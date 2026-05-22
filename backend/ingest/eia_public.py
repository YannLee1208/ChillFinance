"""EIA 免 Key dnav XLS 数据适配器。"""

from datetime import UTC, date, datetime
from decimal import Decimal, InvalidOperation
from io import BytesIO
from typing import Any

import httpx
import pandas as pd

from backend.constant import EIA_PUBLIC_SERIES
from backend.domain.models import IndicatorDefinition, Observation


class EIAPublicProvider:
    """从 EIA dnav 历史 XLS 拉取公开石油周频序列。"""

    name = "eia_public"

    def __init__(
        self,
        timeout_seconds: int = 20,
        user_agent: str = "local-macro-monitor/0.1",
    ) -> None:
        self.timeout_seconds = timeout_seconds
        self.user_agent = user_agent

    def supports(self, indicator: IndicatorDefinition) -> bool:
        """判断指标是否配置了 EIA 公开 XLS 序列。"""

        return indicator.code in EIA_PUBLIC_SERIES

    async def fetch(self, indicator: IndicatorDefinition) -> list[Observation]:
        """下载 EIA XLS 并转换为统一观察值。"""

        config = EIA_PUBLIC_SERIES[indicator.code]
        series_id = config["series_id"]
        url = f"https://www.eia.gov/dnav/pet/hist_xls/{series_id.lower()}w.xls"
        async with httpx.AsyncClient(
            timeout=self.timeout_seconds,
            headers={"User-Agent": self.user_agent},
            follow_redirects=True,
        ) as client:
            response = await client.get(url)
            response.raise_for_status()
        return parse_eia_public_xls(
            content=response.content,
            indicator=indicator,
            source=config["source"],
        )


def parse_eia_public_xls(
    *,
    content: bytes,
    indicator: IndicatorDefinition,
    source: str,
) -> list[Observation]:
    """解析 EIA dnav XLS 的 Data 1 工作表。"""

    frame = pd.read_excel(BytesIO(content), sheet_name=1)
    if len(frame.columns) < 2:
        raise ValueError("EIA XLS must contain date and value columns")

    date_column = frame.columns[0]
    value_column = frame.columns[1]
    ingested_at = datetime.now(UTC)
    observations: list[Observation] = []
    for _, row in frame.iterrows():
        period_value = row[date_column]
        raw_value = row[value_column]
        if _is_missing(period_value) or _is_missing(raw_value):
            continue
        period = _parse_period(period_value)
        if period is None:
            continue
        observations.append(
            Observation(
                indicator_code=indicator.code,
                period=period,
                value=_to_decimal(raw_value),
                provider=EIAPublicProvider.name,
                source=source,
                ingested_at=ingested_at,
            )
        )
    return sorted(observations, key=lambda observation: observation.period)


def _parse_period(value: Any) -> date | None:
    if isinstance(value, pd.Timestamp):
        return value.date()
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value

    text = str(value).strip()
    try:
        return datetime.strptime(text[:10], "%Y-%m-%d").date()
    except ValueError:
        return None


def _is_missing(value: Any) -> bool:
    return value is None or value == "" or bool(pd.isna(value))


def _to_decimal(value: Any) -> Decimal:
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"Invalid numeric value from EIA XLS: {value}") from exc
