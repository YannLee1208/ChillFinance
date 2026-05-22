"""EIA 公开 XLS 解析测试。"""

from decimal import Decimal
from io import BytesIO

import pandas as pd

from backend.domain.catalog import get_indicator
from backend.ingest.eia_public import parse_eia_public_xls


def test_parse_eia_public_xls_skips_header_rows() -> None:
    buffer = BytesIO()
    frame = pd.DataFrame(
        {
            "Back to Contents": [
                "Sourcekey",
                "Date",
                pd.Timestamp("2026-05-09"),
                pd.Timestamp("2026-05-16"),
            ],
            "Data 1: Weekly U.S. Ending Stocks excluding SPR of Crude Oil  (Thousand Barrels)": [
                "WCESTUS1",
                "Weekly U.S. Ending Stocks excluding SPR of Crude Oil  (Thousand Barrels)",
                441800,
                443200,
            ],
        }
    )
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        pd.DataFrame({"contents": ["ignored"]}).to_excel(writer, index=False, sheet_name="Contents")
        frame.to_excel(writer, index=False, sheet_name="Data 1")

    observations = parse_eia_public_xls(
        content=buffer.getvalue(),
        indicator=get_indicator("EIA_US_CRUDE_STOCKS_EX_SPR"),
        source="EIA dnav:WCESTUS1",
    )

    assert [observation.period.isoformat() for observation in observations] == [
        "2026-05-09",
        "2026-05-16",
    ]
    assert observations[1].value == Decimal("443200")
    assert observations[1].provider == "eia_public"
