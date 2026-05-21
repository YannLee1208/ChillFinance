"""指标目录测试。"""

from backend.domain.catalog import get_catalog, get_indicator


def test_catalog_contains_requested_domains() -> None:
    catalog = get_catalog()
    domains = {indicator.domain for indicator in catalog}

    assert {
        "rates",
        "country_macro",
        "nonferrous",
        "crude_oil",
        "coal",
        "power",
    }.issubset(domains)


def test_us_treasury_indicator_has_frequency_and_unit() -> None:
    indicator = get_indicator("US_DGS10")

    assert indicator.name == "U.S. Treasury 10Y yield"
    assert indicator.domain == "rates"
    assert indicator.region == "United States"
    assert indicator.frequency == "daily"
    assert indicator.unit == "%"
    assert indicator.provider == "fred"
    assert indicator.source == "FRED:DGS10"
    assert indicator.display_order == 4


def test_catalog_codes_are_unique() -> None:
    catalog = get_catalog()
    codes = [indicator.code for indicator in catalog]

    assert len(codes) == len(set(codes))
