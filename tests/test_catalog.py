"""指标目录测试。"""

from backend.domain.catalog import get_catalog, get_indicator


def test_catalog_contains_requested_domains() -> None:
    catalog = get_catalog()
    domains = {indicator.domain for indicator in catalog}

    assert {
        "rates",
        "china_macro",
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
        indicator.domain == "china_macro" and indicator.selectors.get("country") == "China"
        for indicator in catalog
    )
    assert not any(
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
    assert indicator.domain == "china_macro"
    assert indicator.availability.status == "pending_source"
    assert "月度实际 GDP" in indicator.availability.reason
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
    pbc_codes = {
        "CN_TOTAL_SOCIAL_FINANCING",
        "CN_TOTAL_SOCIAL_FINANCING_STOCK",
        "CN_RMB_LOANS",
        "CN_RMB_LOAN_BALANCE",
        "CN_HOUSEHOLD_LOAN_INCREMENT",
        "CN_HOUSEHOLD_SHORT_TERM_LOAN_INCREMENT",
        "CN_HOUSEHOLD_MEDIUM_LONG_TERM_LOAN_INCREMENT",
    }
    akshare_codes = {
        "CN_M2",
        "CN_M2_YOY",
        "CN_M1",
        "CN_M1_YOY",
        "CN_M0",
        "CN_M0_YOY",
        "CN_M1_M2_SCISSORS",
    }

    for code in pbc_codes:
        indicator = get_indicator(code)
        assert indicator.provider == "pbc_public"
        assert indicator.availability.status == "available"
        assert indicator.domain == "china_macro"
        assert indicator.selectors.get("category") == "汇率与金融"

    for code in akshare_codes:
        indicator = get_indicator(code)
        assert indicator.provider == "akshare_china"
        assert indicator.availability.status == "available"
        assert indicator.domain == "china_macro"
        assert indicator.selectors.get("category") == "汇率与金融"


def test_china_macro_credit_indicators_define_comparison_groups() -> None:
    expected = {
        "CN_HOUSEHOLD_LOAN_INCREMENT",
        "CN_HOUSEHOLD_SHORT_TERM_LOAN_INCREMENT",
        "CN_HOUSEHOLD_MEDIUM_LONG_TERM_LOAN_INCREMENT",
    }

    for code in expected:
        indicator = get_indicator(code)
        assert indicator.selectors.get("compare_group") == "贷款增量"
    assert get_indicator("CN_RMB_LOANS").selectors.get("compare_group") == "信用增量总览"


def test_pboc_public_table_subitems_are_discoverable() -> None:
    expected = {
        "CN_SF_RMB_LOAN_FLOW": "社融增量结构",
        "CN_SF_GOVERNMENT_BOND_FLOW": "社融增量结构",
        "CN_SF_RMB_LOAN_STOCK": "社融存量结构",
        "CN_SF_GOVERNMENT_BOND_STOCK": "社融存量结构",
        "CN_RMB_DEPOSIT_BALANCE": "存贷款余额",
        "CN_HOUSEHOLD_LOAN_BALANCE": "贷款余额结构",
        "CN_ENTERPRISE_LOAN_INCREMENT": "贷款增量",
        "CN_ENTERPRISE_SHORT_TERM_LOAN_INCREMENT": "企业贷款增量结构",
    }

    for code, compare_group in expected.items():
        indicator = get_indicator(code)
        assert indicator.domain == "china_macro"
        assert indicator.provider == "pbc_public"
        assert indicator.availability.status == "available"
        assert indicator.selectors.get("compare_group") == compare_group


def test_china_cpi_ppi_order_and_mom_comparison_group() -> None:
    expected_order = [
        "CN_CPI_MONTHLY_INDEX",
        "CN_CPI_MONTHLY_YOY",
        "CN_CPI_MONTHLY_MOM",
        "CN_PPI_INDEX",
        "CN_PPI",
        "CN_PPI_MOM",
    ]

    indicators = [get_indicator(code) for code in expected_order]
    assert [indicator.display_order for indicator in indicators] == sorted(
        indicator.display_order for indicator in indicators
    )
    assert get_indicator("CN_CPI_MONTHLY_MOM").selectors.get("compare_group") == "CPI/PPI环比"
    assert get_indicator("CN_PPI_MOM").selectors.get("compare_group") == "CPI/PPI环比"
    assert get_indicator("CN_CPI_MONTHLY_INDEX").selectors.get("metric") == "CPI指数"
    assert get_indicator("CN_CPI_MONTHLY_MOM").selectors.get("metric") == "CPI环比"
    assert get_indicator("CN_CPI_MONTHLY_MOM").selectors.get("display_group") == "CPI"
    assert get_indicator("CN_PPI_INDEX").selectors.get("metric") == "PPI指数"
    assert get_indicator("CN_PPI_ACCUMULATED_INDEX").selectors.get("metric") == "PPI累计指数"
    assert get_indicator("CN_PPI_MOM").selectors.get("display_group") == "PPI"


def test_annual_cpi_inflation_is_not_mixed_with_monthly_cpi_ppi() -> None:
    indicator = get_indicator("CN_CPI_INFLATION")

    assert indicator.frequency == "annual"
    assert indicator.provider == "world_bank"
    assert indicator.selectors.get("metric") == "年度CPI通胀率"
    assert indicator.selectors.get("display_group") == "其他价格指标"


def test_china_price_trade_topic_uses_row_groups_and_chart_styles() -> None:
    expected = {
        "CN_CPI_MONTHLY_INDEX": ("CPI", "price"),
        "CN_CPI_MONTHLY_YOY": ("CPI", "price"),
        "CN_CPI_MONTHLY_MOM": ("CPI", "price"),
        "CN_PPI_INDEX": ("PPI", "price"),
        "CN_PPI": ("PPI", "price"),
        "CN_PPI_MOM": ("PPI", "price"),
        "CN_PPI_ACCUMULATED_INDEX": ("PPI", "price"),
        "CN_EXPORT_VALUE_USD": ("出口", "trade"),
        "CN_EXPORT_YOY_USD": ("出口", "trade"),
        "CN_EXPORTS_GOODS_SERVICES": ("出口", "trade"),
        "CN_IMPORT_VALUE_USD": ("进口", "trade"),
        "CN_IMPORT_YOY_USD": ("进口", "trade"),
        "CN_IMPORTS_GOODS_SERVICES": ("进口", "trade"),
    }

    for code, (display_group, chart_style) in expected.items():
        indicator = get_indicator(code)
        assert indicator.selectors.get("category") == "价格与进出口"
        assert indicator.selectors.get("display_group") == display_group
        assert indicator.selectors.get("chart_style") == chart_style


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
        assert indicator.selectors.get("category") == "\u4ef7\u683c\u4e0e\u8fdb\u51fa\u53e3"


def test_nbs_price_indicators_use_public_akshare_provider() -> None:
    for code in {"CN_CPI_MONTHLY_YOY", "CN_PPI", "CN_PPI_INDEX", "CN_PPI_ACCUMULATED_INDEX"}:
        indicator = get_indicator(code)
        assert indicator.provider == "akshare_china"
        assert indicator.availability.status == "available"
        assert indicator.selectors.get("country") == "China"
        assert indicator.selectors.get("category") == "\u4ef7\u683c\u4e0e\u8fdb\u51fa\u53e3"


def test_cross_sector_public_indicators_are_discoverable() -> None:
    expected = {
        "LME_COPPER_INVENTORY": ("akshare_china", "nonferrous"),
        "LME_ALUMINUM_INVENTORY": ("akshare_china", "nonferrous"),
        "LME_ZINC_INVENTORY": ("akshare_china", "nonferrous"),
        "LME_NICKEL_INVENTORY": ("akshare_china", "nonferrous"),
        "COMEX_GOLD_INVENTORY": ("akshare_china", "nonferrous"),
        "SHFE_COPPER_INVENTORY": ("akshare_china", "nonferrous"),
        "CN_SOCIETY_ELECTRICITY": ("nea_public", "power"),
        "CN_SOCIETY_ELECTRICITY_YOY": ("nea_public", "power"),
        "CN_ENERGY_INDEX": ("akshare_china", "power"),
    }

    for code, (provider, domain) in expected.items():
        indicator = get_indicator(code)
        assert indicator.provider == provider
        assert indicator.domain == domain
        assert indicator.availability.status == "available"


def test_nonferrous_exchange_indicators_are_discoverable() -> None:
    expected = {
        "SHFE_COPPER_FUTURES_CLOSE",
        "SHFE_COPPER_FUTURES_SETTLE",
        "SHFE_ALUMINUM_FUTURES_CLOSE",
        "SHFE_ZINC_FUTURES_CLOSE",
        "SHFE_LEAD_FUTURES_CLOSE",
        "SHFE_NICKEL_FUTURES_CLOSE",
        "SHFE_TIN_FUTURES_CLOSE",
        "SHFE_ALUMINA_FUTURES_CLOSE",
        "GFEX_INDUSTRIAL_SILICON_FUTURES_CLOSE",
        "INE_BONDED_COPPER_FUTURES_CLOSE",
        "SHFE_COPPER_INVENTORY_DAILY",
        "SHFE_COPPER_99QH_INVENTORY",
        "SHFE_ALUMINUM_99QH_INVENTORY",
        "SHFE_ZINC_99QH_INVENTORY",
        "SHFE_NICKEL_99QH_INVENTORY",
        "SHFE_LEAD_99QH_INVENTORY",
        "CN_COMMODITY_PRICE_INDEX",
    }

    for code in expected:
        indicator = get_indicator(code)
        assert indicator.provider == "akshare_china"
        assert indicator.domain == "nonferrous"
        assert indicator.availability.status == "available"
        assert "market" not in indicator.selectors
        assert indicator.selectors.get("display_group")


def test_country_macro_price_trade_topic_is_merged() -> None:
    country_macro = [
        indicator for indicator in get_catalog() if indicator.domain == "country_macro"
    ]

    assert all(indicator.selectors.get("country") for indicator in country_macro)
    assert not any(
        indicator.selectors.get("category") in {"\u4ef7\u683c", "\u8fdb\u51fa\u53e3\u4ef7\u683c"}
        for indicator in country_macro
    )
    assert any(
        indicator.selectors.get("category") == "\u4ef7\u683c\u4e0e\u8fdb\u51fa\u53e3"
        for indicator in country_macro
    )


def test_china_price_trade_titles_include_country() -> None:
    price_trade_indicators = [
        indicator
        for indicator in get_catalog()
        if indicator.domain == "china_macro"
        and indicator.selectors.get("country") == "China"
        and indicator.selectors.get("category") == "\u4ef7\u683c\u4e0e\u8fdb\u51fa\u53e3"
    ]

    assert price_trade_indicators
    assert all(indicator.name.startswith("China ") for indicator in price_trade_indicators)


def test_gold_indicators_are_expanded() -> None:
    expected = {
        "CN_PBOC_GOLD_RESERVE",
        "CN_PBOC_FX_RESERVE",
        "CN_GOLD_ETF_HOLDINGS",
        "SGE_AU9999_CLOSE",
        "SGE_GOLD_BENCHMARK_PM",
        "SHFE_GOLD_FUTURES_CLOSE",
        "SHFE_GOLD_FUTURES_SETTLE",
        "SHFE_SILVER_FUTURES_CLOSE",
        "SHFE_SILVER_FUTURES_SETTLE",
        "CN_SILVER_ETF_HOLDINGS",
        "CN_SILVER_ETF_HOLDINGS_CHANGE",
        "SGE_AG9999_CLOSE",
        "SGE_SILVER_BENCHMARK_PM",
    }

    for code in expected:
        indicator = get_indicator(code)
        assert indicator.provider == "akshare_china"
        assert indicator.domain == "nonferrous"
        assert indicator.availability.status == "available"
        if "SILVER" in code or code == "SGE_AG9999_CLOSE":
            assert indicator.selectors.get("commodity") == "Silver"
        else:
            assert indicator.selectors.get("commodity") == "Gold"


def test_nonferrous_splits_gold_and_silver_commodities() -> None:
    commodities = {
        indicator.selectors.get("commodity")
        for indicator in get_catalog()
        if indicator.domain == "nonferrous"
    }

    assert {"Gold", "Silver"}.issubset(commodities)


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


def test_route_level_tanker_indicators_are_documented() -> None:
    expected = {
        "TD3C_TANKER_FREIGHT",
        "TD7_TANKER_FREIGHT",
        "TD8_TANKER_FREIGHT",
        "TD9_TANKER_FREIGHT",
        "TD14_TANKER_FREIGHT",
        "TD15_TANKER_FREIGHT",
        "TD19_TANKER_FREIGHT",
        "TD20_TANKER_FREIGHT",
        "TD22_TANKER_FREIGHT",
        "TD25_TANKER_FREIGHT",
        "TC2_TANKER_FREIGHT",
        "TC5_TANKER_FREIGHT",
        "TC6_TANKER_FREIGHT",
        "TC8_TANKER_FREIGHT",
        "TC14_TANKER_FREIGHT",
        "TC17_TANKER_FREIGHT",
        "TC20_TANKER_FREIGHT",
    }

    for code in expected:
        indicator = get_indicator(code)
        assert indicator.provider == "unavailable"
        assert indicator.domain == "oil_shipping"
        assert indicator.availability.status == "pending_source"
        assert "Baltic" in indicator.availability.next_step
        assert "中远海能" in indicator.availability.next_step


def test_eia_public_petroleum_indicators_are_discoverable() -> None:
    expected = {
        "EIA_US_CRUDE_STOCKS_EX_SPR",
        "EIA_US_TOTAL_CRUDE_STOCKS",
        "EIA_CUSHING_CRUDE_STOCKS",
        "EIA_US_SPR_CRUDE_STOCKS",
        "EIA_US_CRUDE_PRODUCTION",
        "EIA_LOWER48_CRUDE_PRODUCTION",
        "EIA_US_CRUDE_IMPORTS",
        "EIA_US_CRUDE_EXPORTS",
        "EIA_US_REFINERY_CRUDE_INPUTS",
        "EIA_US_REFINERY_UTILIZATION",
        "EIA_US_TOTAL_GASOLINE_STOCKS",
        "EIA_US_DISTILLATE_STOCKS",
        "EIA_US_JET_FUEL_STOCKS",
        "EIA_US_TOTAL_PETROLEUM_STOCKS",
    }

    for code in expected:
        indicator = get_indicator(code)
        assert indicator.provider == "eia_public"
        assert indicator.domain == "crude_oil"
        assert indicator.availability.status == "available"


def test_coal_futures_and_inventory_indicators_are_discoverable() -> None:
    expected = {
        "CN_COKING_COAL_FUTURES_CLOSE": ("akshare_china", "coal"),
        "CN_COKING_COAL_FUTURES_SETTLE": ("akshare_china", "coal"),
        "CN_COKE_FUTURES_CLOSE": ("akshare_china", "coal"),
        "CN_COKE_FUTURES_SETTLE": ("akshare_china", "coal"),
        "CN_COKING_COAL_99QH_INVENTORY": ("akshare_china", "coal"),
        "CN_COKE_99QH_INVENTORY": ("akshare_china", "coal"),
        "CN_METHANOL_99QH_INVENTORY": ("akshare_china", "coal"),
    }

    for code, (provider, domain) in expected.items():
        indicator = get_indicator(code)
        assert indicator.provider == provider
        assert indicator.domain == domain
        assert indicator.availability.status == "available"

    thermal_coal = get_indicator("CN_THERMAL_COAL_FUTURES_CLOSE")
    assert thermal_coal.provider == "unavailable"
    assert thermal_coal.availability.status == "pending_source"
    assert "2022" in thermal_coal.availability.reason


def test_power_consumption_and_carbon_indicators_are_discoverable() -> None:
    nea_expected = {
        "CN_PRIMARY_INDUSTRY_ELECTRICITY",
        "CN_PRIMARY_INDUSTRY_ELECTRICITY_YOY",
        "CN_SECONDARY_INDUSTRY_ELECTRICITY",
        "CN_SECONDARY_INDUSTRY_ELECTRICITY_YOY",
        "CN_TERTIARY_INDUSTRY_ELECTRICITY",
        "CN_TERTIARY_INDUSTRY_ELECTRICITY_YOY",
        "CN_RESIDENTIAL_ELECTRICITY",
        "CN_RESIDENTIAL_ELECTRICITY_YOY",
    }
    akshare_expected = {
        "CN_BEIJING_CARBON_AVG_PRICE",
        "CN_HUBEI_CARBON_PRICE",
    }

    for code in nea_expected:
        indicator = get_indicator(code)
        assert indicator.provider == "nea_public"
        assert indicator.domain == "power"
        assert indicator.availability.status == "available"
        assert indicator.selectors.get("display_group") == "\u7528\u7535\u91cf"

    for code in akshare_expected:
        indicator = get_indicator(code)
        assert indicator.provider == "akshare_china"
        assert indicator.domain == "power"
        assert indicator.availability.status == "available"
        assert indicator.selectors.get("display_group") == "\u78b3\u4ef7"

    for code in {
        "CN_THERMAL_POWER_GENERATION",
        "CN_HYDRO_POWER_GENERATION",
        "CN_WIND_POWER_GENERATION",
        "CN_SOLAR_POWER_GENERATION",
        "CN_NUCLEAR_POWER_GENERATION",
    }:
        indicator = get_indicator(code)
        assert indicator.provider == "askci_public"
        assert indicator.domain == "power"
        assert indicator.availability.status == "available"
        assert indicator.selectors.get("display_group") == "\u53d1\u7535\u7ed3\u6784"


def test_additional_macro_indicators_are_discoverable() -> None:
    expected = {
        "CN_MANUFACTURING_PMI": ("akshare_china", "china_macro"),
        "CN_NON_MANUFACTURING_PMI": ("akshare_china", "china_macro"),
        "CN_CORPORATE_GOODS_PRICE_INDEX": ("akshare_china", "china_macro"),
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
