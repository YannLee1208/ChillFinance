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
    assert indicator.provider == "us_treasury"
    assert indicator.source == "U.S. Treasury Daily Treasury Rates:10 Yr"
    assert indicator.display_order == 4
    assert indicator.selectors == {
        "country": "United States",
        "tenor": "10Y",
        "metric": "Yield",
    }


def test_catalog_replaces_seed_with_public_providers() -> None:
    catalog = get_catalog()
    providers = {indicator.provider for indicator in catalog}

    assert "seed" not in providers
    assert {"china_data", "fred", "unavailable", "us_treasury", "world_bank"}.issubset(providers)


def test_catalog_has_filterable_dimensions() -> None:
    catalog = get_catalog()

    assert all(indicator.selectors for indicator in catalog)
    assert any(
        indicator.domain == "nonferrous" and indicator.selectors.get("commodity") == "Copper"
        for indicator in catalog
    )
    assert any(
        indicator.domain == "country_macro" and indicator.selectors.get("country") == "China"
        for indicator in catalog
    )
    assert any(indicator.code == "CN_M2" for indicator in catalog)
    assert any(indicator.code == "CN_M1_M2_SCISSORS" for indicator in catalog)
    assert any(
        indicator.code == "CN_RETAIL_SALES"
        and indicator.selectors.get("category") == "消费"
        for indicator in catalog
    )
    assert any(
        indicator.code == "CN_OFFICIAL_EXCHANGE_RATE"
        and indicator.provider == "world_bank"
        for indicator in catalog
    )


def test_catalog_codes_are_unique() -> None:
    catalog = get_catalog()
    codes = [indicator.code for indicator in catalog]

    assert len(codes) == len(set(codes))
