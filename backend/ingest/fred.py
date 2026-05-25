"""FRED 数据解析与美国国债收益率适配器。"""

import asyncio
import shutil
import subprocess
from datetime import UTC, date, datetime
from decimal import Decimal, InvalidOperation
from io import StringIO
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import pandas as pd

from backend.constant import FRED_SERIES
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


class FredSeriesProvider:
    """从 FRED 拉取通用时间序列。"""

    name = "fred"

    def __init__(self, timeout_seconds: int, user_agent: str) -> None:
        self.timeout_seconds = timeout_seconds
        self.user_agent = user_agent

    def supports(self, indicator: IndicatorDefinition) -> bool:
        """判断指标是否属于已配置的 FRED 序列。"""

        return indicator.code in FRED_SERIES

    async def fetch(self, indicator: IndicatorDefinition) -> list[Observation]:
        """从 FRED 下载 CSV 并解析为观测值列表。"""

        fred_code = FRED_SERIES[indicator.code]
        url = "https://fred.stlouisfed.org/graph/fredgraph.csv"
        headers = {"User-Agent": self.user_agent}
        params = {"id": fred_code, "observation_start": _default_start_date().isoformat()}

        response_text = await asyncio.to_thread(
            _fetch_fred_csv,
            url,
            params,
            headers,
            self.timeout_seconds,
        )

        return parse_fred_csv(
            csv_text=response_text,
            indicator_code=indicator.code,
            provider=self.name,
            source=indicator.source,
        )


FredTreasuryProvider = FredSeriesProvider


def _is_missing_value(value: object) -> bool:
    if pd.isna(value):
        return True
    return str(value).strip() in {"", "."}


def _default_start_date() -> date:
    """限制默认拉取窗口，避免本地启动时下载过长历史。"""

    today = datetime.now(UTC).date()
    return date(today.year - 10, 1, 1)


def _fetch_fred_csv(
    url: str,
    params: dict[str, str],
    headers: dict[str, str],
    timeout_seconds: int,
) -> str:
    request_url = f"{url}?{urlencode(params)}"
    curl_bin = shutil.which("curl") or shutil.which("curl.exe")
    if curl_bin is not None:
        return _fetch_fred_csv_with_curl(curl_bin, request_url, timeout_seconds)

    request = Request(request_url, headers=headers)
    try:
        with urlopen(request, timeout=timeout_seconds) as response:  # noqa: S310
            return response.read().decode("utf-8")
    except (TimeoutError, URLError):
        raise


def _fetch_fred_csv_with_curl(
    curl_bin: str,
    request_url: str,
    timeout_seconds: int,
) -> str:
    completed = subprocess.run(
        [
            curl_bin,
            "-L",
            "--silent",
            "--show-error",
            "--max-time",
            str(timeout_seconds),
            request_url,
        ],
        check=True,
        capture_output=True,
        text=True,
        timeout=timeout_seconds + 5,
    )
    return completed.stdout
