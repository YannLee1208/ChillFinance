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
    assert {"akshare_china", "fred", "unavailable", "us_treasury", "world_bank"}.issubset(
        providers
    )


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
    assert any(
        indicator.code == "CN_M1_M2_SCISSORS" and indicator.provider == "akshare_china"
        for indicator in catalog
    )
    assert any(
        indicator.code == "CN_RETAIL_SALES"
        and indicator.provider == "akshare_china"
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


def test_unavailable_indicators_explain_status_and_next_step() -> None:
    indicator = get_indicator("CN_REAL_GDP")

    assert indicator.provider == "unavailable"
    assert indicator.availability.status == "blocked"
    assert "403" in indicator.availability.reason
    assert "Wind" in indicator.availability.next_step


def test_available_indicators_default_to_available_status() -> None:
    indicator = get_indicator("CN_M2")

    assert indicator.provider == "akshare_china"
    assert indicator.availability.status == "available"
    assert indicator.availability.reason == ""


def test_china_fiscal_indicators_mark_world_bank_no_data() -> None:
    debt_indicator = get_indicator("CN_DEBT_TO_GDP")
    fiscal_indicator = get_indicator("CN_FISCAL_BALANCE_TO_GDP")

    assert debt_indicator.provider == "world_bank"
    assert debt_indicator.availability.status == "no_data"
    assert "World Bank" in debt_indicator.availability.reason
    assert fiscal_indicator.availability.status == "no_data"
    assert "财政部" in fiscal_indicator.availability.next_step


def test_key_gated_and_exchange_indicators_are_discoverable() -> None:
    eia_indicator = get_indicator("US_EIA_CRUDE_STOCKS")
    lme_indicator = get_indicator("LME_COPPER_INVENTORY")
    shfe_indicator = get_indicator("SHFE_COPPER_INVENTORY")

    assert eia_indicator.domain == "crude_oil"
    assert eia_indicator.provider == "unavailable"
    assert eia_indicator.availability.status == "needs_key"
    assert "EIA_API_KEY" in eia_indicator.availability.next_step
    assert lme_indicator.domain == "nonferrous"
    assert lme_indicator.availability.status == "pending_source"
    assert shfe_indicator.domain == "nonferrous"
    assert shfe_indicator.availability.status == "pending_source"


def test_pboc_financing_and_money_indicators_use_public_data_provider() -> None:
    expected_codes = {
        "CN_TOTAL_SOCIAL_FINANCING",
        "CN_RMB_LOANS",
        "CN_M2",
        "CN_M2_YOY",
        "CN_M1",
        "CN_M1_YOY",
        "CN_M0",
        "CN_M0_YOY",
        "CN_M1_M2_SCISSORS",
    }

    for code in expected_codes:
        indicator = get_indicator(code)
        assert indicator.provider == "akshare_china"
        assert indicator.availability.status == "available"
        assert indicator.selectors.get("category") == "汇率与金融"
