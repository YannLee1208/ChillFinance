"""基于已入库序列计算派生宏观指标。"""

import calendar
from datetime import UTC, date, datetime
from decimal import Decimal

from backend.domain.models import IndicatorDefinition, Observation

_EXPORT_SERIES_CODE = "CN_EXPORT_VALUE_USD"
_IMPORT_SERIES_CODE = "CN_IMPORT_VALUE_USD"
_GOODS_SERVICES_EXPORT_SERIES_CODE = "CN_EXPORTS_GOODS_SERVICES"
_GOODS_SERVICES_IMPORT_SERIES_CODE = "CN_IMPORTS_GOODS_SERVICES"


def build_local_derived_series(
    definition: IndicatorDefinition,
    source_series: dict[str, list[Observation]],
) -> list[Observation]:
    """用已入库的基础序列计算本地派生指标。"""

    if definition.code == "CN_EXPORT_MOM_USD":
        return _change_observations(definition, source_series.get(_EXPORT_SERIES_CODE, []), 1)
    if definition.code == "CN_IMPORT_MOM_USD":
        return _change_observations(definition, source_series.get(_IMPORT_SERIES_CODE, []), 1)
    if definition.code == "CN_TRADE_BALANCE_USD":
        return _balance_observations(definition, source_series)
    if definition.code == "CN_TRADE_BALANCE_MOM_USD":
        return _change_observations(definition, _balance_observations(definition, source_series), 1)
    if definition.code == "CN_TRADE_BALANCE_YOY_USD":
        return _change_observations(
            definition,
            _balance_observations(definition, source_series),
            12,
        )
    if definition.code == "CN_GOODS_SERVICES_TRADE_BALANCE":
        return _balance_observations(
            definition,
            source_series,
            _GOODS_SERVICES_EXPORT_SERIES_CODE,
            _GOODS_SERVICES_IMPORT_SERIES_CODE,
        )
    return []


def required_source_codes(indicator_code: str) -> set[str]:
    """返回派生指标依赖的基础指标代码。"""

    if indicator_code == "CN_EXPORT_MOM_USD":
        return {_EXPORT_SERIES_CODE}
    if indicator_code == "CN_IMPORT_MOM_USD":
        return {_IMPORT_SERIES_CODE}
    if indicator_code in {
        "CN_TRADE_BALANCE_USD",
        "CN_TRADE_BALANCE_MOM_USD",
        "CN_TRADE_BALANCE_YOY_USD",
    }:
        return {_EXPORT_SERIES_CODE, _IMPORT_SERIES_CODE}
    if indicator_code == "CN_GOODS_SERVICES_TRADE_BALANCE":
        return {_GOODS_SERVICES_EXPORT_SERIES_CODE, _GOODS_SERVICES_IMPORT_SERIES_CODE}
    return set()


def _balance_observations(
    definition: IndicatorDefinition,
    source_series: dict[str, list[Observation]],
    export_series_code: str = _EXPORT_SERIES_CODE,
    import_series_code: str = _IMPORT_SERIES_CODE,
) -> list[Observation]:
    export_values = {
        point.period: point.value
        for point in source_series.get(export_series_code, [])
    }
    import_values = {
        point.period: point.value
        for point in source_series.get(import_series_code, [])
    }
    periods = sorted(set(export_values) & set(import_values))
    ingested_at = _latest_ingested_at(source_series)

    return [
        _observation(definition, period, export_values[period] - import_values[period], ingested_at)
        for period in periods
    ]


def _change_observations(
    definition: IndicatorDefinition,
    source_points: list[Observation],
    months_back: int,
) -> list[Observation]:
    value_by_period = {point.period: point.value for point in source_points}
    ingested_at = _latest_ingested_at({"source": source_points})
    observations: list[Observation] = []
    for point in sorted(source_points, key=lambda item: item.period):
        previous_period = _shift_month(point.period, -months_back)
        previous_value = value_by_period.get(previous_period)
        if previous_value is None or previous_value == 0:
            continue
        value = (point.value - previous_value) / abs(previous_value) * Decimal("100")
        observations.append(_observation(definition, point.period, value, ingested_at))
    return observations


def _observation(
    definition: IndicatorDefinition,
    period: date,
    value: Decimal,
    ingested_at: datetime,
) -> Observation:
    return Observation(
        indicator_code=definition.code,
        period=period,
        value=value,
        provider=definition.provider,
        source=definition.source,
        ingested_at=ingested_at,
    )


def _latest_ingested_at(source_series: dict[str, list[Observation]]) -> datetime:
    latest = max(
        (point.ingested_at for points in source_series.values() for point in points),
        default=None,
    )
    return latest or datetime.now(UTC)


def _shift_month(period: date, month_delta: int) -> date:
    month_index = period.year * 12 + period.month - 1 + month_delta
    year = month_index // 12
    month = month_index % 12 + 1
    day = min(period.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)
