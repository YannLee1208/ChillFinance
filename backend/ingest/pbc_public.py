"""中国人民银行统计数据公开表适配器。"""

from __future__ import annotations

import re
from datetime import UTC, date, datetime
from decimal import Decimal, InvalidOperation
from io import BytesIO
from typing import Any
from urllib.parse import urljoin

import httpx
import pandas as pd

from backend.constant import PBC_PUBLIC_SERIES, PBC_STATS_YEAR_INDEX_PATHS, PBC_STATS_YEAR_START
from backend.domain.models import IndicatorDefinition, Observation

_PBC_BASE_URL = "https://www.pbc.gov.cn"
_PBC_STATS_URL = _PBC_BASE_URL + "/diaochatongjisi/116219/116319/{year}ntjsj/{slug}/index.html"
_PBC_LEGACY_STATS_URL = (
    _PBC_BASE_URL + "/diaochatongjisi/116219/116319/{path}/{legacy_slug}/index.html"
)
_TABLE_SLUGS = {
    "social_financing_flow": "shrzgm",
    "social_financing_stock": "shrzgm",
    "rmb_credit": "jrjgxdsztj",
}
_LEGACY_TABLE_SLUGS = {
    "shrzgm": "4780804",
    "jrjgxdsztj": "4780810",
}
_TABLE_TITLES = {
    "social_financing_flow": "社会融资规模增量统计表",
    "social_financing_stock": "社会融资规模存量统计表",
    "rmb_credit": "金融机构人民币信贷收支表",
}


class PBCPublicProvider:
    """从人民银行年度统计数据页拉取社融和人民币信贷公开表。"""

    name = "pbc_public"

    def __init__(
        self,
        timeout_seconds: int = 20,
        user_agent: str = "local-macro-monitor/0.1",
    ) -> None:
        self.timeout_seconds = timeout_seconds
        self.user_agent = user_agent
        self._frame_cache: dict[tuple[str, int], pd.DataFrame] = {}

    def supports(self, indicator: IndicatorDefinition) -> bool:
        """判断指标是否由人民银行公开统计表提供。"""

        return indicator.provider == self.name and indicator.code in PBC_PUBLIC_SERIES

    async def fetch(self, indicator: IndicatorDefinition) -> list[Observation]:
        """下载 2020 年以来的人民银行年度 xlsx，并解析为观测值。"""

        config = PBC_PUBLIC_SERIES[indicator.code]
        table = config["table"]
        current_year = _current_beijing_year()
        frames = [
            frame
            for year in range(PBC_STATS_YEAR_START, current_year + 1)
            if (frame := await self._fetch_table_frame_or_none(table, year)) is not None
        ]
        if not frames:
            return []

        observations: list[Observation] = []
        for frame in frames:
            observations.extend(
                parse_pbc_public_table(frame=frame, indicator=indicator, config=config)
            )
        return sorted(observations, key=lambda observation: observation.period)

    async def _fetch_table_frame_or_none(self, table: str, year: int) -> pd.DataFrame | None:
        cache_key = (table, year)
        if cache_key in self._frame_cache:
            return self._frame_cache[cache_key]

        page_url = _pbc_stats_page_url(table, year)
        async with httpx.AsyncClient(
            timeout=self.timeout_seconds,
            headers={"User-Agent": self.user_agent},
            follow_redirects=True,
        ) as client:
            page_response = await client.get(page_url)
            if page_response.status_code == 404:
                return None
            page_response.raise_for_status()
            xlsx_url = _select_xlsx_url(page_response.text, page_url, _TABLE_TITLES[table])
            xlsx_response = await client.get(xlsx_url)
            xlsx_response.raise_for_status()

        frame = pd.read_excel(BytesIO(xlsx_response.content), header=None)
        self._frame_cache[cache_key] = frame
        return frame


def parse_pbc_public_table(
    *,
    frame: pd.DataFrame,
    indicator: IndicatorDefinition,
    config: dict[str, str],
) -> list[Observation]:
    """解析人民银行公开 xlsx 表，支持横表和社融增量纵表。"""

    if config["table"] == "social_financing_flow":
        raw_points = _parse_vertical_month_table(frame, config["row_label"])
    elif config["table"] == "social_financing_stock":
        raw_points = _parse_social_financing_stock_table(frame, config["row_label"])
    elif config["table"] == "rmb_credit":
        raw_points = _parse_rmb_credit_table(frame, config["row_label"], config.get("row_context"))
    else:
        raise ValueError(f"Unsupported PBC table: {config['table']}")

    multiplier = _to_decimal(config.get("unit_multiplier", "1"))
    points = [(period, value * multiplier) for period, value in raw_points if value is not None]
    if config.get("value_transform") == "monthly_change":
        points = _to_monthly_change(points)

    ingested_at = datetime.now(UTC)
    return [
        Observation(
            indicator_code=indicator.code,
            period=period,
            value=value,
            provider=PBCPublicProvider.name,
            source=config["source"],
            ingested_at=ingested_at,
        )
        for period, value in points
    ]


def _select_xlsx_url(page_html: str, page_url: str, table_title: str) -> str:
    title_index = page_html.find(table_title)
    if title_index < 0:
        raise ValueError(f"PBC page does not include table title: {table_title}")
    following_html = page_html[title_index:]
    match = re.search(r'href="([^"]+\.xlsx)"', following_html, flags=re.IGNORECASE)
    if match is None:
        raise ValueError(f"PBC page does not include xlsx link for: {table_title}")
    return urljoin(page_url, match.group(1))


def _pbc_stats_page_url(table: str, year: int) -> str:
    slug = _TABLE_SLUGS[table]
    if year in PBC_STATS_YEAR_INDEX_PATHS:
        legacy_slug = _LEGACY_TABLE_SLUGS[slug]
        if slug == "jrjgxdsztj":
            # 2023 归档页的信贷收支统计仅暴露了子表，无法稳定定位全表。
            return _PBC_STATS_URL.format(year=year, slug=slug)
        return _PBC_LEGACY_STATS_URL.format(
            path=PBC_STATS_YEAR_INDEX_PATHS[year],
            legacy_slug=legacy_slug,
        )
    return _PBC_STATS_URL.format(year=year, slug=slug)


def _parse_vertical_month_table(
    frame: pd.DataFrame,
    value_column_name: str,
) -> list[tuple[date, Decimal]]:
    header_row = _find_row_index(frame, "月份")
    value_column = _find_column_index(frame, header_row, value_column_name)
    period_column = _find_column_index(frame, header_row, "月份")

    points: list[tuple[date, Decimal]] = []
    for row_index in range(header_row + 1, len(frame)):
        period = _parse_year_month(frame.iat[row_index, period_column])
        try:
            value = _decimal_or_none(frame.iat[row_index, value_column])
        except ValueError:
            continue
        if period is not None and value is not None:
            points.append((period, value))
    return sorted(points, key=lambda item: item[0])


def _parse_social_financing_stock_table(
    frame: pd.DataFrame,
    row_label: str,
) -> list[tuple[date, Decimal]]:
    month_row = _find_month_header_row(frame)
    value_row = _find_row_index(frame, row_label)

    points: list[tuple[date, Decimal]] = []
    for column_index in range(1, frame.shape[1]):
        period = _parse_year_month(frame.iat[month_row, column_index])
        if period is None:
            continue
        try:
            value = _decimal_or_none(frame.iat[value_row, column_index])
        except ValueError:
            continue
        if value is not None:
            points.append((period, value))
    return sorted(points, key=lambda item: item[0])


def _parse_rmb_credit_table(
    frame: pd.DataFrame,
    row_label: str,
    row_context: str | None,
) -> list[tuple[date, Decimal]]:
    header_row = _find_row_index(frame, "项目 Item")
    value_row = _find_credit_row_index(frame, row_label, row_context)

    points: list[tuple[date, Decimal]] = []
    for column_index in range(1, frame.shape[1]):
        period = _parse_year_month(frame.iat[header_row, column_index])
        try:
            value = _decimal_or_none(frame.iat[value_row, column_index])
        except ValueError:
            continue
        if period is not None and value is not None:
            points.append((period, value))
    return sorted(points, key=lambda item: item[0])


def _find_row_index(frame: pd.DataFrame, needle: str) -> int:
    normalized_needle = _normalize_label(needle)
    candidate: int | None = None
    for row_index in range(len(frame)):
        row_values = frame.iloc[row_index].tolist()
        row_text = _normalize_label(" ".join(str(value) for value in row_values))
        first_cell = _normalize_label(frame.iat[row_index, 0])
        if first_cell == normalized_needle:
            return row_index
        if row_index > 0 and normalized_needle in first_cell:
            candidate = row_index
        if normalized_needle in row_text:
            candidate = row_index
    if candidate is not None:
        return candidate
    raise ValueError(f"PBC table is missing row containing: {needle}")


def _find_column_index(frame: pd.DataFrame, row_index: int, needle: str) -> int:
    normalized_needle = _normalize_label(needle)
    for column_index, value in enumerate(frame.iloc[row_index].tolist()):
        if normalized_needle in _normalize_label(value):
            return column_index
    raise ValueError(f"PBC table is missing column containing: {needle}")


def _find_credit_row_index(frame: pd.DataFrame, row_label: str, row_context: str | None) -> int:
    normalized_row_label = _normalize_label(row_label)
    normalized_row_context = _normalize_label(row_context) if row_context else None
    in_context = row_context is None
    for row_index in range(len(frame)):
        row_text = _normalize_label(frame.iat[row_index, 0])
        if normalized_row_context is not None and normalized_row_context in row_text:
            in_context = True
            continue
        if in_context and normalized_row_label in row_text:
            return row_index
    raise ValueError(f"PBC credit table is missing row: {row_label}")


def _find_month_header_row(frame: pd.DataFrame) -> int:
    for row_index in range(len(frame)):
        if any(_parse_year_month(value) is not None for value in frame.iloc[row_index].tolist()):
            return row_index
    raise ValueError("PBC table is missing month header row")


def _to_monthly_change(points: list[tuple[date, Decimal]]) -> list[tuple[date, Decimal]]:
    changes: list[tuple[date, Decimal]] = []
    previous_value: Decimal | None = None
    for period, value in sorted(points, key=lambda item: item[0]):
        if previous_value is not None:
            changes.append((period, value - previous_value))
        previous_value = value
    return changes


def _parse_year_month(value: Any) -> date | None:
    if _is_missing(value):
        return None
    text = str(value).strip()
    match = re.search(r"(?P<year>20\d{2})[.\-/年](?P<month>\d{1,2})", text)
    if match is None:
        return None
    return date(int(match.group("year")), int(match.group("month")), 1)


def _current_beijing_year() -> int:
    """按北京时间判断当前统计年份，避免 UTC 年末跨日影响。"""

    return datetime.now().year


def _decimal_or_none(value: Any) -> Decimal | None:
    if _is_missing(value):
        return None
    return _to_decimal(value)


def _to_decimal(value: Any) -> Decimal:
    text = str(value).strip().replace(",", "")
    if text.endswith("%"):
        text = text[:-1]
    try:
        return Decimal(text)
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"Invalid numeric value from PBC: {value}") from exc


def _normalize_label(value: Any) -> str:
    return re.sub(r"\s+", "", str(value).replace("\xa0", " ").strip())


def _is_missing(value: Any) -> bool:
    return value is None or value == "" or bool(pd.isna(value))
