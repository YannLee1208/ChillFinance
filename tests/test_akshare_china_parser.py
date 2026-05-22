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
