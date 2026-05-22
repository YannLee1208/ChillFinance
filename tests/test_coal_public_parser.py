"""公开煤炭数据解析测试。"""

from decimal import Decimal

from backend.ingest.coal_public import (
    parse_cctd_price_payload,
    parse_cfd_history_payload,
    parse_cfd_latest_payload,
)


def test_parse_cctd_price_payload_selects_value_field() -> None:
    payload = [
        {"name": "2026-05-13", "age": "1061", "age1": "1061"},
        {"name": "2026-05-20", "age": "1064", "age1": "1064"},
    ]

    observations = parse_cctd_price_payload(
        payload=payload,
        indicator_code="CCTD_HUANGLING_QI_COAL",
        provider="coal_public",
        source="CCTD:/Echarts/data/CCTD_PRICE_HL.php:age",
        value_field="age",
    )

    assert observations[-1].period.isoformat() == "2026-05-20"
    assert observations[-1].value == Decimal("1064")


def test_parse_cfd_latest_payload_uses_public_date() -> None:
    payload = {
        "data": {
            "ts_index": {
                "public_date": "2026-05-21",
                "k5500": "835.00",
            }
        }
    }

    observations = parse_cfd_latest_payload(
        payload=payload,
        indicator_code="CFD_TTCI_THERMAL_COAL_5500",
        provider="coal_public",
        source="CFDCoal:/api/indexs/home:ts_index.k5500",
        section="ts_index",
        date_field="public_date",
        value_field="k5500",
    )

    assert observations[0].period.isoformat() == "2026-05-21"
    assert observations[0].value == Decimal("835.00")


def test_parse_cfd_history_payload_pairs_reversed_lists() -> None:
    payload = {
        "data": {
            "ts_index_date": ["2026-05-21", "2026-05-20"],
            "ts_index_9999": ["1597.50", "1597.50"],
        }
    }

    observations = parse_cfd_history_payload(
        payload=payload,
        indicator_code="CFD_TTCI_INDEX",
        provider="coal_public",
        source="CFDCoal:/api/indexs/home:ts_index_9999",
        date_list_key="ts_index_date",
        value_list_key="ts_index_9999",
    )

    assert observations[0].period.isoformat() == "2026-05-20"
    assert observations[1].period.isoformat() == "2026-05-21"
    assert observations[1].value == Decimal("1597.50")
