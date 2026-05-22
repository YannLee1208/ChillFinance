"""中商产业研究院公开数据页适配器。"""

import html as html_lib
import re
from datetime import UTC, date, datetime
from decimal import Decimal, InvalidOperation
from typing import Any

import httpx

from backend.constant import ASKCI_PUBLIC_SERIES
from backend.domain.models import IndicatorDefinition, Observation

_ASKCI_ENERGY_URL = "https://s.askci.com/data/energy/{indicator}/"
_VALUE_INDEX = {
    "monthly_value": 2,
    "cumulative_value": 3,
    "monthly_yoy": 4,
    "cumulative_yoy": 5,
}


class AskciPublicProvider:
    """从中商公开数据页拉取 NBS 月度产量表。"""

    name = "askci_public"

    def __init__(
        self,
        timeout_seconds: int = 20,
        user_agent: str = "local-macro-monitor/0.1",
    ) -> None:
        self.timeout_seconds = timeout_seconds
        self.user_agent = user_agent

    def supports(self, indicator: IndicatorDefinition) -> bool:
        """判断指标是否配置了中商公开数据页。"""

        return indicator.provider == self.name and indicator.code in ASKCI_PUBLIC_SERIES

    async def fetch(self, indicator: IndicatorDefinition) -> list[Observation]:
        """下载中商公开表格并转换为统一观察值。"""

        config = ASKCI_PUBLIC_SERIES[indicator.code]
        indicator_id = config["indicator"]
        url = _ASKCI_ENERGY_URL.format(indicator=indicator_id)
        async with httpx.AsyncClient(
            timeout=self.timeout_seconds,
            headers={"User-Agent": self.user_agent},
            follow_redirects=True,
        ) as client:
            response = await client.get(url)
            response.raise_for_status()

        return parse_askci_monthly_output_table(
            html=response.text,
            indicator=indicator,
            source=f"中商产业研究院/NBS:{indicator_id}:{url}",
            value_kind=config["value_kind"],
        )


def parse_askci_monthly_output_table(
    *,
    html: str,
    indicator: IndicatorDefinition,
    source: str,
    value_kind: str,
) -> list[Observation]:
    """解析中商月度产量表。"""

    value_index = _VALUE_INDEX[value_kind]
    rows = re.findall(r"<tr[^>]*>(.*?)</tr>", html, flags=re.IGNORECASE | re.DOTALL)
    ingested_at = datetime.now(UTC)
    observations: list[Observation] = []
    for row_html in rows:
        cells = [
            _clean_cell(cell)
            for cell in re.findall(
                r"<t[dh][^>]*>(.*?)</t[dh]>",
                row_html,
                re.IGNORECASE | re.DOTALL,
            )
        ]
        if len(cells) <= value_index:
            continue
        period = _parse_chinese_month(cells[1])
        if period is None:
            continue
        value_text = cells[value_index]
        if not value_text or value_text == "--":
            continue
        observations.append(
            Observation(
                indicator_code=indicator.code,
                period=period,
                value=_to_decimal(value_text),
                provider=AskciPublicProvider.name,
                source=source,
                ingested_at=ingested_at,
            )
        )
    return sorted(observations, key=lambda observation: observation.period)


def _clean_cell(cell_html: str) -> str:
    without_tags = re.sub(r"<[^>]+>", "", cell_html)
    return html_lib.unescape(without_tags).strip()


def _parse_chinese_month(value: str) -> date | None:
    match = re.search(r"(?P<year>\d{4})年(?P<month>\d{1,2})月", value)
    if match is None:
        return None
    return date(int(match.group("year")), int(match.group("month")), 1)


def _to_decimal(value: Any) -> Decimal:
    try:
        return Decimal(str(value).replace(",", ""))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"中商公开数据页数值无效: {value}") from exc
