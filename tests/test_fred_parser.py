"""FRED 解析测试。"""

from decimal import Decimal

from backend.ingest.fred import parse_fred_csv


def test_parse_fred_csv_skips_missing_values() -> None:
    csv_text = "DATE,DGS10\n2026-01-01,4.10\n2026-01-02,.\n2026-01-03,4.12\n"

    observations = parse_fred_csv(
        csv_text=csv_text,
        indicator_code="US_DGS10",
        provider="fred",
        source="FRED:DGS10",
    )

    assert len(observations) == 2
    assert observations[0].value == Decimal("4.10")
    assert observations[1].value == Decimal("4.12")
