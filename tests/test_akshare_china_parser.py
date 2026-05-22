"""AkShare 中国宏观解析测试。"""

import json
from decimal import Decimal

import pandas as pd

from backend.constant import AKSHARE_CHINA_SERIES
from backend.domain.catalog import get_indicator
from backend.ingest.akshare_china import AkShareChinaProvider, parse_akshare_series_frame


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


def test_parse_year_month_period() -> None:
    frame = pd.DataFrame(
        {
            "月份": ["2026-04", "2026-03"],
            "新增人民币贷款-总额": [-100.0, 29952.24],
        }
    )
    indicator = get_indicator("CN_RMB_LOANS")

    observations = parse_akshare_series_frame(
        frame=frame,
        indicator=indicator,
        config={
            "date_column": "月份",
            "value_column": "新增人民币贷款-总额",
            "source": "AKShare/10jqka:macro_rmb_loan",
            "period_type": "year_month",
        },
    )

    assert observations[0].period.isoformat() == "2026-03-01"
    assert observations[1].period.isoformat() == "2026-04-01"
    assert observations[1].value == Decimal("-100.0")


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


def test_parse_power_consumption_decimal_month_with_multiplier() -> None:
    frame = pd.DataFrame(
        {
            "统计时间": ["2026.3", "2026.4"],
            "第二产业用电量": [159870000.0, 215690000.0],
        }
    )
    indicator = get_indicator("CN_SECONDARY_INDUSTRY_ELECTRICITY")

    observations = parse_akshare_series_frame(
        frame=frame,
        indicator=indicator,
        config={
            "date_column": "统计时间",
            "value_column": "第二产业用电量",
            "source": "AKShare/Sina:macro_china_society_electricity:secondary",
            "period_type": "decimal_month",
            "multiplier": "0.0001",
        },
    )

    assert observations[0].period.isoformat() == "2026-03-01"
    assert observations[1].value == Decimal("21569.00000")


def test_parse_carbon_market_daily_price() -> None:
    frame = pd.DataFrame(
        {
            "日期": ["2026-05-08", "2026-05-11"],
            "成交价": [37.19, 37.50],
        }
    )
    indicator = get_indicator("CN_HUBEI_CARBON_PRICE")

    observations = parse_akshare_series_frame(
        frame=frame,
        indicator=indicator,
        config={
            "date_column": "日期",
            "value_column": "成交价",
            "source": "AKShare/Hubei:energy_carbon_hb",
            "period_type": "date",
        },
    )

    assert observations[0].period.isoformat() == "2026-05-08"
    assert observations[1].value == Decimal("37.5")


async def test_provider_reuses_same_akshare_frame(monkeypatch) -> None:
    call_count = 0

    def fake_call_akshare(config: dict[str, str]) -> pd.DataFrame:
        nonlocal call_count
        call_count += 1
        return pd.DataFrame(
            {
                config["date_column"]: ["2026.4"],
                AKSHARE_CHINA_SERIES["CN_SOCIETY_ELECTRICITY"]["value_column"]: [
                    77210000.0
                ],
                AKSHARE_CHINA_SERIES["CN_SOCIETY_ELECTRICITY_YOY"]["value_column"]: [4.7],
            }
        )

    monkeypatch.setattr("backend.ingest.akshare_china._call_akshare", fake_call_akshare)
    provider = AkShareChinaProvider()

    total = await provider.fetch(get_indicator("CN_SOCIETY_ELECTRICITY"))
    yoy = await provider.fetch(get_indicator("CN_SOCIETY_ELECTRICITY_YOY"))

    assert call_count == 1
    assert total[0].value == Decimal("7721.00000")
    assert yoy[0].value == Decimal("4.7")


async def test_provider_retries_empty_json_response(monkeypatch) -> None:
    call_count = 0

    def fake_akshare() -> pd.DataFrame:
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise json.JSONDecodeError("No value to decode", "", 0)
        config = AKSHARE_CHINA_SERIES["CN_SOCIETY_ELECTRICITY"]
        return pd.DataFrame(
            {
                config["date_column"]: ["2026.4"],
                AKSHARE_CHINA_SERIES["CN_SOCIETY_ELECTRICITY"]["value_column"]: [
                    77210000.0
                ],
            }
        )

    monkeypatch.setattr("backend.ingest.akshare_china.time.sleep", lambda _: None)
    monkeypatch.setattr(
        "backend.ingest.akshare_china.ak.macro_china_society_electricity",
        fake_akshare,
    )

    provider = AkShareChinaProvider()
    observations = await provider.fetch(get_indicator("CN_SOCIETY_ELECTRICITY"))

    assert call_count == 3
    assert observations[0].value == Decimal("7721.00000")


async def test_provider_computes_ppi_mom_from_index(monkeypatch) -> None:
    def fake_call_akshare(config: dict[str, str]) -> pd.DataFrame:
        return pd.DataFrame(
            {
                config["date_column"]: ["2026年03月份", "2026年04月份"],
                "当月": [99.8, 100.1],
            }
        )

    monkeypatch.setattr("backend.ingest.akshare_china._call_akshare", fake_call_akshare)
    provider = AkShareChinaProvider()

    observations = await provider.fetch(get_indicator("CN_PPI_MOM"))

    assert observations[0].period.isoformat() == "2026-04-01"
    assert observations[0].value.quantize(Decimal("0.000001")) == Decimal("0.300601")
