"""AkShare 中国宏观解析测试。"""

from decimal import Decimal

import pandas as pd

from backend.domain.catalog import get_indicator
from backend.ingest.akshare_china import parse_akshare_series_frame


def test_parse_decimal_month_period() -> None:
    frame = pd.DataFrame(
        {
            "统计时间": [2026.4, 2026.3],
            "社会融资规模存量": [427.22, 425.87],
        }
    )
    indicator = get_indicator("CN_TOTAL_SOCIAL_FINANCING")

    observations = parse_akshare_series_frame(
        frame=frame,
        indicator=indicator,
        config={
            "date_column": "统计时间",
            "value_column": "社会融资规模存量",
            "source": "AKShare/PBOC:macro_china_shrzgm:stock",
            "period_type": "decimal_month",
            "multiplier": "10000",
        },
    )

    assert observations[0].period.isoformat() == "2026-03-01"
    assert observations[1].period.isoformat() == "2026-04-01"
    assert observations[1].value == Decimal("4272200")


def test_parse_decimal_month_keeps_two_digit_month() -> None:
    frame = pd.DataFrame(
        {
            "统计时间": ["2004.10", "2004.12"],
            "全社会用电量": [175828690.0, 217350000.0],
        }
    )
    indicator = get_indicator("CN_TOTAL_SOCIAL_FINANCING")

    observations = parse_akshare_series_frame(
        frame=frame,
        indicator=indicator,
        config={
            "date_column": "统计时间",
            "value_column": "全社会用电量",
            "source": "AKShare/Sina:macro_china_society_electricity",
            "period_type": "decimal_month",
        },
    )

    assert observations[0].period.isoformat() == "2004-10-01"
    assert observations[1].period.isoformat() == "2004-12-01"


def test_parse_customs_monthly_amount_with_multiplier() -> None:
    frame = pd.DataFrame(
        {
            "月份": ["2026年04月份", "2026年03月份"],
            "当月出口额-金额": [359442100.0, 321045200.0],
        }
    )
    indicator = get_indicator("CN_EXPORT_VALUE_USD")

    observations = parse_akshare_series_frame(
        frame=frame,
        indicator=indicator,
        config={
            "date_column": "月份",
            "value_column": "当月出口额-金额",
            "source": "AKShare/Customs:macro_china_hgjck",
            "period_type": "month",
            "multiplier": "0.00001",
        },
    )

    assert observations[0].period.isoformat() == "2026-03-01"
    assert observations[1].period.isoformat() == "2026-04-01"
    assert observations[1].value == Decimal("3594.421000")


def test_parse_sina_futures_daily_close() -> None:
    frame = pd.DataFrame(
        {
            "date": ["2026-05-21", "2026-05-22"],
            "close": [1190.5, 1162.5],
            "settle": [1207.0, 1173.0],
        }
    )
    indicator = get_indicator("CN_COKING_COAL_FUTURES_CLOSE")

    observations = parse_akshare_series_frame(
        frame=frame,
        indicator=indicator,
        config={
            "date_column": "date",
            "value_column": "close",
            "source": "AKShare/Sina:futures_zh_daily_sina:JM0:close",
            "period_type": "date",
        },
    )

    assert observations[0].period.isoformat() == "2026-05-21"
    assert observations[1].value == Decimal("1162.5")


def test_parse_99qh_inventory() -> None:
    frame = pd.DataFrame(
        {
            "日期": ["2026-05-21", "2026-05-22"],
            "收盘价": [1190.5, 1162.5],
            "库存": [500, 200],
        }
    )
    indicator = get_indicator("CN_COKING_COAL_99QH_INVENTORY")

    observations = parse_akshare_series_frame(
        frame=frame,
        indicator=indicator,
        config={
            "date_column": "日期",
            "value_column": "库存",
            "source": "AKShare/99qh:futures_inventory_99:焦煤:库存",
            "period_type": "date",
        },
    )

    assert observations[0].period.isoformat() == "2026-05-21"
    assert observations[1].value == Decimal("200")
