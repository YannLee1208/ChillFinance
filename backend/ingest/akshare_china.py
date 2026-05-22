"""AkShare 中国宏观与市场数据适配器。"""

import calendar
from datetime import UTC, date, datetime
from decimal import Decimal, InvalidOperation
from typing import Any

import akshare as ak
import pandas as pd

from backend.constant import AKSHARE_CHINA_SERIES
from backend.domain.models import IndicatorDefinition, Observation


class AkShareChinaProvider:
    """从 AkShare 支持的公开源抓取中国宏观和市场序列。"""

    name = "akshare_china"

    def supports(self, indicator: IndicatorDefinition) -> bool:
        """判断指标是否配置了 AkShare 中国数据源。"""

        return indicator.code in AKSHARE_CHINA_SERIES

    async def fetch(self, indicator: IndicatorDefinition) -> list[Observation]:
        """拉取 AkShare DataFrame 并转换为统一观察值。"""

        config = AKSHARE_CHINA_SERIES[indicator.code]
        frame = _call_akshare(config)
        if config.get("computed") == "m1_yoy_minus_m2_yoy":
            return _parse_m1_m2_scissors(frame, indicator)
        if config.get("aggregate") == "mean_by_date":
            return _parse_mean_by_date(frame, indicator, config)
        return _parse_series_frame(frame, indicator, config)


def _call_akshare(config: dict[str, str]) -> pd.DataFrame:
    function_name = config["function"]
    function = getattr(ak, function_name)
    if "symbol" in config:
        frame = function(symbol=config["symbol"])
    else:
        frame = function()
    if not isinstance(frame, pd.DataFrame):
        raise ValueError(f"AkShare {function_name} did not return a DataFrame")
    if frame.empty:
        raise ValueError(f"AkShare {function_name} returned an empty DataFrame")
    return frame


def _parse_series_frame(
    frame: pd.DataFrame,
    indicator: IndicatorDefinition,
    config: dict[str, str],
) -> list[Observation]:
    date_column = config["date_column"]
    value_column = config["value_column"]
    _ensure_columns(frame, [date_column, value_column])

    ingested_at = datetime.now(UTC)
    observations: list[Observation] = []
    for _, row in frame.iterrows():
        period_value = row[date_column]
        raw_value = row[value_column]
        if _is_missing(period_value) or _is_missing(raw_value):
            continue
        observations.append(
            _build_observation(
                indicator=indicator,
                period=_parse_period(period_value, config["period_type"]),
                value=_to_decimal(raw_value),
                source=config["source"],
                ingested_at=ingested_at,
            )
        )
    return sorted(observations, key=lambda observation: observation.period)


def _parse_mean_by_date(
    frame: pd.DataFrame,
    indicator: IndicatorDefinition,
    config: dict[str, str],
) -> list[Observation]:
    date_column = config["date_column"]
    value_column = config["value_column"]
    _ensure_columns(frame, [date_column, value_column])

    valid_frame = frame[[date_column, value_column]].copy()
    valid_frame = valid_frame.dropna(subset=[date_column, value_column])
    if valid_frame.empty:
        return []
    grouped = valid_frame.groupby(date_column, as_index=False)[value_column].mean(numeric_only=True)

    return _parse_series_frame(grouped, indicator, config)


def _parse_m1_m2_scissors(
    frame: pd.DataFrame,
    indicator: IndicatorDefinition,
) -> list[Observation]:
    date_column = "月份"
    m1_column = "货币(M1)-同比增长"
    m2_column = "货币和准货币(M2)-同比增长"
    _ensure_columns(frame, [date_column, m1_column, m2_column])

    ingested_at = datetime.now(UTC)
    observations: list[Observation] = []
    for _, row in frame.iterrows():
        has_missing_value = (
            _is_missing(row[date_column])
            or _is_missing(row[m1_column])
            or _is_missing(row[m2_column])
        )
        if has_missing_value:
            continue
        observations.append(
            _build_observation(
                indicator=indicator,
                period=_parse_period(row[date_column], "month"),
                value=_to_decimal(row[m1_column]) - _to_decimal(row[m2_column]),
                source=AKSHARE_CHINA_SERIES[indicator.code]["source"],
                ingested_at=ingested_at,
            )
        )
    return sorted(observations, key=lambda observation: observation.period)


def _build_observation(
    *,
    indicator: IndicatorDefinition,
    period: date,
    value: Decimal,
    source: str,
    ingested_at: datetime,
) -> Observation:
    return Observation(
        indicator_code=indicator.code,
        period=period,
        value=value,
        provider=AkShareChinaProvider.name,
        source=source,
        ingested_at=ingested_at,
    )


def _ensure_columns(frame: pd.DataFrame, required_columns: list[str]) -> None:
    missing_columns = [column for column in required_columns if column not in frame.columns]
    if missing_columns:
        raise ValueError(f"AkShare response is missing columns: {', '.join(missing_columns)}")


def _is_missing(value: Any) -> bool:
    return value is None or value == "" or bool(pd.isna(value))


def _to_decimal(value: Any) -> Decimal:
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"Invalid numeric value from AkShare: {value}") from exc


def _parse_period(value: Any, period_type: str) -> date:
    if isinstance(value, pd.Timestamp):
        return value.date()
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value

    text = str(value).strip()
    if period_type == "month":
        return datetime.strptime(text, "%Y年%m月份").date()
    if period_type == "quarter":
        return _parse_chinese_quarter(text)
    if period_type == "date":
        return datetime.strptime(text[:10], "%Y-%m-%d").date()
    raise ValueError(f"Unsupported AkShare period type: {period_type}")


def _parse_chinese_quarter(text: str) -> date:
    year_text, quarter_text = text.split("年第")
    year = int(year_text)
    quarter_part = quarter_text.replace("季度", "")
    quarter = int(quarter_part.split("-")[-1])
    month = quarter * 3
    day = calendar.monthrange(year, month)[1]
    return date(year, month, day)
