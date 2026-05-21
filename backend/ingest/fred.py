"""FRED 数据解析与美国国债收益率适配器。"""

from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation
from io import StringIO

import httpx
import pandas as pd

from backend.constant import FRED_TREASURY_SERIES
from backend.domain.models import IndicatorDefinition, Observation


def parse_fred_csv(
    csv_text: str,
    indicator_code: str,
    provider: str,
    source: str,
) -> list[Observation]:
    """解析 FRED CSV 文本为观测值列表。"""

    frame = pd.read_csv(StringIO(csv_text))
    if len(frame.columns) < 2:
        raise ValueError("FRED CSV must contain at least two columns")

    date_column = frame.columns[0]
    value_column = frame.columns[1]
    ingested_at = datetime.now(UTC)
    observations: list[Observation] = []

    for row in frame.itertuples(index=False):
        period_text = getattr(row, date_column)
        value_text = getattr(row, value_column)
        if _is_missing_value(value_text):
            continue

        try:
            value = Decimal(str(value_text))
        except InvalidOperation as exc:
            raise ValueError(f"Invalid FRED value: {value_text}") from exc

        observations.append(
            Observation(
                indicator_code=indicator_code,
                period=pd.to_datetime(period_text).date(),
                value=value,
                provider=provider,
                source=source,
                ingested_at=ingested_at,
            )
        )

    return observations


class FredTreasuryProvider:
    """从 FRED 拉取美国国债收益率序列。"""

    name = "fred"

    def __init__(self, timeout_seconds: int, user_agent: str) -> None:
        self.timeout_seconds = timeout_seconds
        self.user_agent = user_agent

    def supports(self, indicator: IndicatorDefinition) -> bool:
        """判断指标是否属于 FRED 国债收益率序列。"""

        return indicator.code in FRED_TREASURY_SERIES

    async def fetch(self, indicator: IndicatorDefinition) -> list[Observation]:
        """从 FRED 下载 CSV 并解析为观测值列表。"""

        fred_code = FRED_TREASURY_SERIES[indicator.code]
        url = "https://fred.stlouisfed.org/graph/fredgraph.csv"
        headers = {"User-Agent": self.user_agent}
        params = {"id": fred_code}

        async with httpx.AsyncClient(timeout=self.timeout_seconds, headers=headers) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()

        return parse_fred_csv(
            csv_text=response.text,
            indicator_code=indicator.code,
            provider=self.name,
            source=indicator.source,
        )


def _is_missing_value(value: object) -> bool:
    if pd.isna(value):
        return True
    return str(value).strip() in {"", "."}
