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
    assert lme_indicator.provider == "akshare_china"
    assert lme_indicator.availability.status == "available"
    assert shfe_indicator.domain == "nonferrous"
    assert shfe_indicator.provider == "akshare_china"
    assert shfe_indicator.availability.status == "available"


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


def test_customs_trade_indicators_use_public_customs_table() -> None:
    expected_codes = {
        "CN_EXPORT_VALUE_USD",
        "CN_IMPORT_VALUE_USD",
        "CN_EXPORT_YOY_USD",
        "CN_IMPORT_YOY_USD",
    }

    for code in expected_codes:
        indicator = get_indicator(code)
        assert indicator.provider == "akshare_china"
        assert indicator.availability.status == "available"
        assert "Customs" in indicator.source
        assert indicator.selectors.get("category") == "进出口价格"


def test_nbs_price_indicators_use_public_akshare_provider() -> None:
    for code in {"CN_CPI_MONTHLY_YOY", "CN_PPI"}:
        indicator = get_indicator(code)
        assert indicator.provider == "akshare_china"
        assert indicator.availability.status == "available"
        assert indicator.selectors.get("country") == "China"


def test_cross_sector_public_indicators_are_discoverable() -> None:
    expected = {
        "LME_COPPER_INVENTORY": ("akshare_china", "nonferrous"),
        "LME_ALUMINUM_INVENTORY": ("akshare_china", "nonferrous"),
        "LME_ZINC_INVENTORY": ("akshare_china", "nonferrous"),
        "LME_NICKEL_INVENTORY": ("akshare_china", "nonferrous"),
        "COMEX_GOLD_INVENTORY": ("akshare_china", "nonferrous"),
        "SHFE_COPPER_INVENTORY": ("akshare_china", "nonferrous"),
        "CN_SOCIETY_ELECTRICITY": ("akshare_china", "power"),
        "CN_SOCIETY_ELECTRICITY_YOY": ("akshare_china", "power"),
        "CN_ENERGY_INDEX": ("akshare_china", "power"),
    }

    for code, (provider, domain) in expected.items():
        indicator = get_indicator(code)
        assert indicator.provider == provider
        assert indicator.domain == domain
        assert indicator.availability.status == "available"


def test_stale_crude_inventory_event_sources_are_not_marked_available() -> None:
    for code in {"US_API_CRUDE_STOCK_CHANGE", "US_EIA_CRUDE_STOCK_CHANGE"}:
        indicator = get_indicator(code)
        assert indicator.domain == "crude_oil"
        assert indicator.provider == "unavailable"
        assert indicator.availability.status == "pending_source"
        assert "停更" in indicator.availability.reason


def test_current_crude_and_tanker_indicators_are_discoverable() -> None:
    expected = {
        "US_CRUDE_OIL_PRODUCTION": ("akshare_china", "crude_oil"),
        "US_CRUDE_OIL_PRODUCTION_CHANGE": ("akshare_china", "crude_oil"),
        "CN_GASOLINE_RETAIL_PRICE": ("akshare_china", "crude_oil"),
        "CN_DIESEL_RETAIL_PRICE": ("akshare_china", "crude_oil"),
        "BDTI_INDEX": ("akshare_china", "oil_shipping"),
        "BCTI_INDEX": ("akshare_china", "oil_shipping"),
        "BDI_INDEX": ("akshare_china", "oil_shipping"),
        "BCI_INDEX": ("akshare_china", "oil_shipping"),
        "BPI_INDEX": ("akshare_china", "oil_shipping"),
    }

    for code, (provider, domain) in expected.items():
        indicator = get_indicator(code)
        assert indicator.provider == provider
        assert indicator.domain == domain
        assert indicator.availability.status == "available"


def test_additional_macro_indicators_are_discoverable() -> None:
    expected = {
        "CN_MANUFACTURING_PMI": ("akshare_china", "country_macro"),
        "CN_NON_MANUFACTURING_PMI": ("akshare_china", "country_macro"),
        "CN_CORPORATE_GOODS_PRICE_INDEX": ("akshare_china", "country_macro"),
        "US_ISM_MANUFACTURING_PMI": ("akshare_china", "country_macro"),
        "US_UNEMPLOYMENT_RATE": ("akshare_china", "country_macro"),
        "US_NONFARM_PAYROLLS": ("akshare_china", "country_macro"),
        "US_CPI_YOY": ("akshare_china", "country_macro"),
        "US_CORE_PCE_YOY": ("akshare_china", "country_macro"),
        "US_RETAIL_SALES_MOM": ("akshare_china", "country_macro"),
    }

    for code, (provider, domain) in expected.items():
        indicator = get_indicator(code)
        assert indicator.provider == provider
        assert indicator.domain == domain
        assert indicator.availability.status == "available"


def test_coal_price_indicators_are_discoverable() -> None:
    available_expected = {
        "CCTD_HUANGLING_QI_COAL",
        "CCTD_QHD_THERMAL_COAL_5500",
        "CCTD_QHD_THERMAL_COAL_5000",
        "CCTD_QHD_THERMAL_COAL_4500",
        "CCTD_TANGSHAN_COKING_COAL",
        "CCTD_TANGSHAN_FAT_COAL",
        "CCTD_ORIGIN_SHANXI_THERMAL_COAL_5500",
        "CFD_TTCI_THERMAL_COAL_5500",
        "CFD_TTCI_THERMAL_COAL_5000",
        "CFD_TTCI_THERMAL_COAL_4500",
        "CFD_TTCI_INDEX",
        "CFD_TOFI_INDEX",
    }

    for code in available_expected:
        indicator = get_indicator(code)
        assert indicator.domain == "coal"
        assert indicator.provider == "coal_public"
        assert indicator.availability.status == "available"


def test_requested_mine_coal_prices_explain_missing_public_source() -> None:
    for code in {"CN_XIAOBAODANG_MIXED_COAL_5500", "CN_HONGLIULIN_WASHED_MIDDLE_LUMP"}:
        indicator = get_indicator(code)
        assert indicator.domain == "coal"
        assert indicator.provider == "unavailable"
        assert indicator.availability.status == "pending_source"
        assert "稳定" in indicator.availability.reason
