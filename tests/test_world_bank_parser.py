"""World Bank 数据解析测试。"""

from decimal import Decimal

from backend.ingest.world_bank import parse_world_bank_payload


def test_parse_world_bank_payload_skips_missing_and_sorts() -> None:
    payload = [
        {"page": 1},
        [
            {"date": "2025", "value": "12.3"},
            {"date": "2024", "value": None},
            {"date": "2023", "value": "10.1"},
        ],
    ]

    observations = parse_world_bank_payload(
        payload=payload,
        indicator_code="CN_GDP",
        provider="world_bank",
        source="WorldBank:NY.GDP.MKTP.CD",
    )

    assert [observation.period.isoformat() for observation in observations] == [
        "2023-12-31",
        "2025-12-31",
    ]
    assert [observation.value for observation in observations] == [
        Decimal("10.1"),
        Decimal("12.3"),
    ]
