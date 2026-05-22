"""ChinaData.live 解析测试。"""

from decimal import Decimal

from backend.ingest.china_data import parse_china_data_payload


def test_parse_china_data_payload_monthly_series() -> None:
    payload = {
        "success": True,
        "data": {
            "data": [
                {"date": "2026-02", "value": 3492200},
                {"date": "2026-03", "value": 3538600},
            ]
        },
    }

    observations = parse_china_data_payload(
        payload=payload,
        indicator_code="CN_M2",
        provider="china_data",
        source="ChinaData.live:china-m2-money-supply",
    )

    assert len(observations) == 2
    assert observations[0].period.isoformat() == "2026-02-01"
    assert observations[1].value == Decimal("3538600")
