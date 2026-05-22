"""美国财政部国债收益率解析测试。"""

from backend.ingest.us_treasury import _month_codes_since, parse_us_treasury_csv


def test_parse_us_treasury_csv() -> None:
    csv_text = (
        'Date,"1 Mo","1.5 Month","2 Mo","3 Mo","4 Mo","6 Mo","1 Yr","2 Yr",'
        '"3 Yr","5 Yr","7 Yr","10 Yr","20 Yr","30 Yr"\n'
        "05/21/2026,3.72,3.68,3.69,3.68,3.76,3.78,3.83,4.08,4.13,"
        "4.25,4.41,4.57,5.09,5.10\n"
    )

    rows = parse_us_treasury_csv(csv_text)

    assert rows[0]["Date"] == "05/21/2026"
    assert rows[0]["3 Mo"] == "3.68"
    assert rows[0]["10 Yr"] == "4.57"


def test_month_codes_since_covers_backfill_window() -> None:
    month_codes = list(_month_codes_since(start_year=2020))

    assert month_codes[0] == "202001"
    assert "202605" in month_codes
    assert month_codes == sorted(month_codes)
