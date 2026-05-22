"""人民银行公开统计表解析测试。"""

from decimal import Decimal

import pandas as pd

from backend.constant import PBC_PUBLIC_SERIES
from backend.domain.catalog import get_indicator
from backend.ingest.pbc_public import parse_pbc_public_table


def test_parse_social_financing_flow_table() -> None:
    frame = pd.DataFrame(
        [
            ["社会融资规模增量统计表", None, None],
            ["月份", "社会融资规模增量", "人民币贷款"],
            ["2026.03", 58900, 33000],
            ["2026.04", 6200, 2000],
        ]
    )

    observations = parse_pbc_public_table(
        frame=frame,
        indicator=get_indicator("CN_TOTAL_SOCIAL_FINANCING"),
        config=PBC_PUBLIC_SERIES["CN_TOTAL_SOCIAL_FINANCING"],
    )

    assert [observation.period.isoformat() for observation in observations] == [
        "2026-03-01",
        "2026-04-01",
    ]
    assert observations[-1].value == Decimal("6200")


def test_parse_social_financing_stock_table_converts_trillion_to_100mn() -> None:
    frame = pd.DataFrame(
        [
            ["社会融资规模存量统计表", None, None, None, None],
            [None, "2026.03", None, "2026.04", None],
            ["项目  Items", "存量", "增速（%）", "存量", "增速（%）"],
            ["社会融资规模存量", 422.96, 8.4, 424.00, 8.3],
        ]
    )

    observations = parse_pbc_public_table(
        frame=frame,
        indicator=get_indicator("CN_TOTAL_SOCIAL_FINANCING_STOCK"),
        config=PBC_PUBLIC_SERIES["CN_TOTAL_SOCIAL_FINANCING_STOCK"],
    )

    assert observations[-1].period.isoformat() == "2026-04-01"
    assert observations[-1].value == Decimal("424.00") * Decimal("10000")


def test_parse_rmb_credit_table_balance_and_monthly_change() -> None:
    frame = pd.DataFrame(
        [
            ["金融机构人民币信贷收支表", None, None, None, None],
            ["项目 Item", "2026.01", "2026.02", "2026.03", "2026.04"],
            ["一、各项贷款 Total Loans", 2766180.81, 2775181.27, 2805133.51, 2805018.53],
            ["1.住户贷款 Loans to Households", 837279.32, 830772.39, 835681.33, 827811.62],
            ["（1）短期贷款 Short-term Loans", 205060.90, 200368.20, 202324.07, 197862.68],
            ["（2） 中长期贷款 Mid & Long-term Loans", 632218.42, 630404.20, 633357.25, 629948.95],
        ]
    )

    balance = parse_pbc_public_table(
        frame=frame,
        indicator=get_indicator("CN_RMB_LOAN_BALANCE"),
        config=PBC_PUBLIC_SERIES["CN_RMB_LOAN_BALANCE"],
    )
    new_loans = parse_pbc_public_table(
        frame=frame,
        indicator=get_indicator("CN_RMB_LOANS"),
        config=PBC_PUBLIC_SERIES["CN_RMB_LOANS"],
    )
    household_short = parse_pbc_public_table(
        frame=frame,
        indicator=get_indicator("CN_HOUSEHOLD_SHORT_TERM_LOAN_INCREMENT"),
        config=PBC_PUBLIC_SERIES["CN_HOUSEHOLD_SHORT_TERM_LOAN_INCREMENT"],
    )

    assert balance[-1].value == Decimal("2805018.53")
    assert new_loans[-1].period.isoformat() == "2026-04-01"
    assert new_loans[-1].value == Decimal("-114.98")
    assert household_short[-1].value == Decimal("-4461.39")


def test_parse_social_financing_flow_subitem() -> None:
    frame = pd.DataFrame(
        [
            ["社会融资规模增量统计表", None, None, None],
            ["月份", "社会融资规模增量", "政府债券", "企业债券"],
            ["2026.03", 52240, 11658, 3910],
            ["2026.04", 6245, 9041, 4520],
        ]
    )

    observations = parse_pbc_public_table(
        frame=frame,
        indicator=get_indicator("CN_SF_GOVERNMENT_BOND_FLOW"),
        config=PBC_PUBLIC_SERIES["CN_SF_GOVERNMENT_BOND_FLOW"],
    )

    assert observations[-1].period.isoformat() == "2026-04-01"
    assert observations[-1].value == Decimal("9041")
