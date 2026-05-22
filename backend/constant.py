"""项目级常量。"""

from pathlib import Path

DEFAULT_DB_PATH = Path("data/macro.duckdb")
DEFAULT_HTTP_TIMEOUT_SECONDS = 20
DEFAULT_USER_AGENT = "local-macro-monitor/0.1"

DATE_FORMAT = "%Y-%m-%d"

FRED_TREASURY_SERIES = {
    "US_DGS3MO": "DGS3MO",
    "US_DGS2": "DGS2",
    "US_DGS5": "DGS5",
    "US_DGS10": "DGS10",
    "US_DGS30": "DGS30",
}

US_TREASURY_SERIES = {
    "US_DGS3MO": "3 Mo",
    "US_DGS2": "2 Yr",
    "US_DGS5": "5 Yr",
    "US_DGS10": "10 Yr",
    "US_DGS30": "30 Yr",
}

FRED_SERIES = {
    "JP_LONG_RATE": "IRLTLT01JPM156N",
    "DE_LONG_RATE": "IRLTLT01DEM156N",
    "EU_LONG_RATE": "IRLTLT01EZM156N",
    "US_GDP": "GDP",
    "US_FEDERAL_DEBT": "GFDEBTN",
    "US_DEBT_TO_GDP": "GFDEGDQ188S",
    "US_FISCAL_BALANCE_TO_GDP": "FYFSGDA188S",
    "CU_PRICE": "PCOPPUSDM",
    "AL_PRICE": "PALUMUSDM",
    "NI_PRICE": "PNICKUSDM",
    "ZN_PRICE": "PZINCUSDM",
    "PB_PRICE": "PLEADUSDM",
    "IRON_ORE_PRICE": "PIORECRUSDM",
    "OIL_BRENT_PRICE": "DCOILBRENTEU",
    "OIL_WTI_PRICE": "DCOILWTICO",
    "US_GASOLINE_PRICE": "GASREGW",
    "EU_NATURAL_GAS_PRICE": "PNGASEUUSDM",
    "COAL_AUSTRALIA_PRICE": "PCOALAUUSDM",
    "US_POWER_PRODUCTION": "IPG2211A2N",
}

WORLD_BANK_SERIES = {
    "CN_GDP": ("CHN", "NY.GDP.MKTP.CD"),
    "CN_REAL_GDP_GROWTH": ("CHN", "NY.GDP.MKTP.KD.ZG"),
    "CN_HOUSEHOLD_CONSUMPTION": ("CHN", "NE.CON.PRVT.CD"),
    "CN_GROSS_CAPITAL_FORMATION": ("CHN", "NE.GDI.TOTL.CD"),
    "CN_INDUSTRY_VALUE_ADDED": ("CHN", "NV.IND.TOTL.CD"),
    "CN_EXPORTS_GOODS_SERVICES": ("CHN", "NE.EXP.GNFS.CD"),
    "CN_IMPORTS_GOODS_SERVICES": ("CHN", "NE.IMP.GNFS.CD"),
    "CN_CPI_INFLATION": ("CHN", "FP.CPI.TOTL.ZG"),
    "CN_OFFICIAL_EXCHANGE_RATE": ("CHN", "PA.NUS.FCRF"),
    "JP_GDP": ("JPN", "NY.GDP.MKTP.CD"),
    "EU_GDP": ("EMU", "NY.GDP.MKTP.CD"),
    "CN_DEBT_TO_GDP": ("CHN", "GC.DOD.TOTL.GD.ZS"),
    "JP_DEBT_TO_GDP": ("JPN", "GC.DOD.TOTL.GD.ZS"),
    "EU_DEBT_TO_GDP": ("EMU", "GC.DOD.TOTL.GD.ZS"),
    "CN_FISCAL_BALANCE_TO_GDP": ("CHN", "GC.NLD.TOTL.GD.ZS"),
    "JP_FISCAL_BALANCE_TO_GDP": ("JPN", "GC.NLD.TOTL.GD.ZS"),
    "EU_FISCAL_BALANCE_TO_GDP": ("EMU", "GC.NLD.TOTL.GD.ZS"),
}

CHINA_DATA_SERIES = {
    "CN_M2": "china-m2-money-supply",
}

COAL_PUBLIC_SERIES = {
    "CCTD_HUANGLING_QI_COAL": {
        "type": "cctd_price",
        "url": "https://www.cctd.com.cn/Echarts/data/CCTD_PRICE_HL.php",
        "value_field": "age",
        "source": "CCTD:/Echarts/data/CCTD_PRICE_HL.php:age",
    },
    "CCTD_QHD_THERMAL_COAL_5500": {
        "type": "cctd_price",
        "url": "https://www.cctd.com.cn/Echarts/data/CCTD_PRICE_QHD.php",
        "value_field": "age",
        "source": "CCTD:/Echarts/data/CCTD_PRICE_QHD.php:age",
    },
    "CCTD_QHD_THERMAL_COAL_5000": {
        "type": "cctd_price",
        "url": "https://www.cctd.com.cn/Echarts/data/CCTD_PRICE_QHD.php",
        "value_field": "age1",
        "source": "CCTD:/Echarts/data/CCTD_PRICE_QHD.php:age1",
    },
    "CCTD_QHD_THERMAL_COAL_4500": {
        "type": "cctd_price",
        "url": "https://www.cctd.com.cn/Echarts/data/CCTD_PRICE_QHD.php",
        "value_field": "age2",
        "source": "CCTD:/Echarts/data/CCTD_PRICE_QHD.php:age2",
    },
    "CCTD_TANGSHAN_COKING_COAL": {
        "type": "cctd_price",
        "url": "https://www.cctd.com.cn/Echarts/data/CCTD_PRICE_TS.php",
        "value_field": "age",
        "source": "CCTD:/Echarts/data/CCTD_PRICE_TS.php:age",
    },
    "CCTD_TANGSHAN_FAT_COAL": {
        "type": "cctd_price",
        "url": "https://www.cctd.com.cn/Echarts/data/CCTD_PRICE_TS.php",
        "value_field": "age1",
        "source": "CCTD:/Echarts/data/CCTD_PRICE_TS.php:age1",
    },
    "CCTD_ORIGIN_SHANXI_THERMAL_COAL_5500": {
        "type": "cctd_price",
        "url": "https://www.cctd.com.cn/Echarts/data/CCTD_PRICE_CD.php",
        "value_field": "age",
        "source": "CCTD:/Echarts/data/CCTD_PRICE_CD.php:age",
    },
    "CFD_TTCI_THERMAL_COAL_5500": {
        "type": "cfd_latest",
        "url": "https://www.cfdcoal.com/api/indexs/home",
        "section": "ts_index",
        "date_field": "public_date",
        "value_field": "k5500",
        "source": "CFDCoal:/api/indexs/home:ts_index.k5500",
    },
    "CFD_TTCI_THERMAL_COAL_5000": {
        "type": "cfd_latest",
        "url": "https://www.cfdcoal.com/api/indexs/home",
        "section": "ts_index",
        "date_field": "public_date",
        "value_field": "k5000",
        "source": "CFDCoal:/api/indexs/home:ts_index.k5000",
    },
    "CFD_TTCI_THERMAL_COAL_4500": {
        "type": "cfd_latest",
        "url": "https://www.cfdcoal.com/api/indexs/home",
        "section": "ts_index",
        "date_field": "public_date",
        "value_field": "k4500",
        "source": "CFDCoal:/api/indexs/home:ts_index.k4500",
    },
    "CFD_TTCI_INDEX": {
        "type": "cfd_history",
        "url": "https://www.cfdcoal.com/api/indexs/home",
        "date_list_key": "ts_index_date",
        "value_list_key": "ts_index_9999",
        "source": "CFDCoal:/api/indexs/home:ts_index_9999",
    },
    "CFD_TOFI_INDEX": {
        "type": "cfd_history",
        "url": "https://www.cfdcoal.com/api/indexs/home",
        "date_list_key": "tofi_index_date",
        "value_list_key": "tofi_index",
        "source": "CFDCoal:/api/indexs/home:tofi_index",
    },
}

EIA_PUBLIC_SERIES = {
    "EIA_US_CRUDE_STOCKS_EX_SPR": {
        "series_id": "WCESTUS1",
        "source": "EIA dnav:WCESTUS1",
    },
    "EIA_US_TOTAL_CRUDE_STOCKS": {
        "series_id": "WCRSTUS1",
        "source": "EIA dnav:WCRSTUS1",
    },
    "EIA_CUSHING_CRUDE_STOCKS": {
        "series_id": "W_EPC0_SAX_YCUOK_MBBL",
        "source": "EIA dnav:W_EPC0_SAX_YCUOK_MBBL",
    },
    "EIA_US_SPR_CRUDE_STOCKS": {
        "series_id": "WCSSTUS1",
        "source": "EIA dnav:WCSSTUS1",
    },
    "EIA_US_CRUDE_PRODUCTION": {
        "series_id": "WCRFPUS2",
        "source": "EIA dnav:WCRFPUS2",
    },
    "EIA_LOWER48_CRUDE_PRODUCTION": {
        "series_id": "W_EPC0_FPF_R48_MBBLD",
        "source": "EIA dnav:W_EPC0_FPF_R48_MBBLD",
    },
    "EIA_US_CRUDE_IMPORTS": {
        "series_id": "WCRIMUS2",
        "source": "EIA dnav:WCRIMUS2",
    },
    "EIA_US_CRUDE_EXPORTS": {
        "series_id": "WCREXUS2",
        "source": "EIA dnav:WCREXUS2",
    },
    "EIA_US_REFINERY_CRUDE_INPUTS": {
        "series_id": "WCRRIUS2",
        "source": "EIA dnav:WCRRIUS2",
    },
    "EIA_US_REFINERY_UTILIZATION": {
        "series_id": "WPULEUS3",
        "source": "EIA dnav:WPULEUS3",
    },
    "EIA_US_TOTAL_GASOLINE_STOCKS": {
        "series_id": "WGTSTUS1",
        "source": "EIA dnav:WGTSTUS1",
    },
    "EIA_US_DISTILLATE_STOCKS": {
        "series_id": "WDISTUS1",
        "source": "EIA dnav:WDISTUS1",
    },
    "EIA_US_JET_FUEL_STOCKS": {
        "series_id": "WKJSTUS1",
        "source": "EIA dnav:WKJSTUS1",
    },
    "EIA_US_TOTAL_PETROLEUM_STOCKS": {
        "series_id": "WTTSTUS1",
        "source": "EIA dnav:WTTSTUS1",
    },
}

AKSHARE_CHINA_SERIES = {
    "CN_NOMINAL_GDP_QUARTERLY": {
        "function": "macro_china_gdp",
        "date_column": "季度",
        "value_column": "国内生产总值-绝对值",
        "source": "AKShare/Eastmoney:macro_china_gdp",
        "period_type": "quarter",
    },
    "CN_REAL_GDP_QUARTERLY_YOY": {
        "function": "macro_china_gdp",
        "date_column": "季度",
        "value_column": "国内生产总值-同比增长",
        "source": "AKShare/Eastmoney:macro_china_gdp",
        "period_type": "quarter",
    },
    "CN_RETAIL_SALES": {
        "function": "macro_china_consumer_goods_retail",
        "date_column": "月份",
        "value_column": "同比增长",
        "source": "AKShare/Eastmoney:macro_china_consumer_goods_retail",
        "period_type": "month",
    },
    "CN_INDUSTRIAL_PRODUCTION_YOY": {
        "function": "macro_china_gyzjz",
        "date_column": "月份",
        "value_column": "同比增长",
        "source": "AKShare/Eastmoney:macro_china_gyzjz",
        "period_type": "month",
    },
    "CN_FIXED_ASSET_INVESTMENT": {
        "function": "macro_china_gdzctz",
        "date_column": "月份",
        "value_column": "同比增长",
        "source": "AKShare/Eastmoney:macro_china_gdzctz",
        "period_type": "month",
    },
    "CN_RMB_LOANS": {
        "function": "macro_china_new_financial_credit",
        "date_column": "月份",
        "value_column": "当月",
        "source": "AKShare/Eastmoney:macro_china_new_financial_credit",
        "period_type": "month",
    },
    "CN_M2": {
        "function": "macro_china_money_supply",
        "date_column": "月份",
        "value_column": "货币和准货币(M2)-数量(亿元)",
        "source": "AKShare/Eastmoney:macro_china_money_supply",
        "period_type": "month",
    },
    "CN_M2_YOY": {
        "function": "macro_china_money_supply",
        "date_column": "月份",
        "value_column": "货币和准货币(M2)-同比增长",
        "source": "AKShare/Eastmoney:macro_china_money_supply",
        "period_type": "month",
    },
    "CN_M1": {
        "function": "macro_china_money_supply",
        "date_column": "月份",
        "value_column": "货币(M1)-数量(亿元)",
        "source": "AKShare/Eastmoney:macro_china_money_supply",
        "period_type": "month",
    },
    "CN_M1_YOY": {
        "function": "macro_china_money_supply",
        "date_column": "月份",
        "value_column": "货币(M1)-同比增长",
        "source": "AKShare/Eastmoney:macro_china_money_supply",
        "period_type": "month",
    },
    "CN_M0": {
        "function": "macro_china_money_supply",
        "date_column": "月份",
        "value_column": "流通中的现金(M0)-数量(亿元)",
        "source": "AKShare/Eastmoney:macro_china_money_supply",
        "period_type": "month",
    },
    "CN_M0_YOY": {
        "function": "macro_china_money_supply",
        "date_column": "月份",
        "value_column": "流通中的现金(M0)-同比增长",
        "source": "AKShare/Eastmoney:macro_china_money_supply",
        "period_type": "month",
    },
    "CN_M1_M2_SCISSORS": {
        "function": "macro_china_money_supply",
        "date_column": "月份",
        "source": "AKShare/Eastmoney:macro_china_money_supply",
        "period_type": "month",
        "computed": "m1_yoy_minus_m2_yoy",
    },
    "CN_NEW_HOME_PRICE_INDEX": {
        "function": "macro_china_new_house_price",
        "date_column": "日期",
        "value_column": "新建商品住宅价格指数-同比",
        "source": "AKShare/Eastmoney:macro_china_new_house_price",
        "period_type": "date",
        "aggregate": "mean_by_date",
    },
    "CN_PPI": {
        "function": "macro_china_ppi",
        "date_column": "月份",
        "value_column": "当月同比增长",
        "source": "AKShare/Eastmoney:macro_china_ppi",
        "period_type": "month",
    },
    "CN_CPI_MONTHLY_YOY": {
        "function": "macro_china_cpi",
        "date_column": "月份",
        "value_column": "全国-同比增长",
        "source": "AKShare/Eastmoney:macro_china_cpi",
        "period_type": "month",
    },
    "CN_EXPORT_VALUE_USD": {
        "function": "macro_china_hgjck",
        "date_column": "月份",
        "value_column": "当月出口额-金额",
        "source": "AKShare/Customs:macro_china_hgjck",
        "period_type": "month",
        "multiplier": "0.00001",
    },
    "CN_IMPORT_VALUE_USD": {
        "function": "macro_china_hgjck",
        "date_column": "月份",
        "value_column": "当月进口额-金额",
        "source": "AKShare/Customs:macro_china_hgjck",
        "period_type": "month",
        "multiplier": "0.00001",
    },
    "CN_EXPORT_YOY_USD": {
        "function": "macro_china_hgjck",
        "date_column": "月份",
        "value_column": "当月出口额-同比增长",
        "source": "AKShare/Customs:macro_china_hgjck",
        "period_type": "month",
    },
    "CN_IMPORT_YOY_USD": {
        "function": "macro_china_hgjck",
        "date_column": "月份",
        "value_column": "当月进口额-同比增长",
        "source": "AKShare/Customs:macro_china_hgjck",
        "period_type": "month",
    },
    "CN_SHCOMP": {
        "function": "stock_zh_index_daily",
        "date_column": "date",
        "value_column": "close",
        "source": "AKShare/Sina:stock_zh_index_daily:sh000001",
        "period_type": "date",
        "symbol": "sh000001",
    },
    "LME_COPPER_INVENTORY": {
        "function": "macro_euro_lme_stock",
        "date_column": "日期",
        "value_column": "铜-库存",
        "source": "AKShare/Jin10:macro_euro_lme_stock",
        "period_type": "date",
    },
    "LME_ALUMINUM_INVENTORY": {
        "function": "macro_euro_lme_stock",
        "date_column": "日期",
        "value_column": "铝-库存",
        "source": "AKShare/Jin10:macro_euro_lme_stock",
        "period_type": "date",
    },
    "LME_ZINC_INVENTORY": {
        "function": "macro_euro_lme_stock",
        "date_column": "日期",
        "value_column": "锌-库存",
        "source": "AKShare/Jin10:macro_euro_lme_stock",
        "period_type": "date",
    },
    "LME_NICKEL_INVENTORY": {
        "function": "macro_euro_lme_stock",
        "date_column": "日期",
        "value_column": "镍-库存",
        "source": "AKShare/Jin10:macro_euro_lme_stock",
        "period_type": "date",
    },
    "SHFE_COPPER_INVENTORY": {
        "function": "futures_inventory_em",
        "date_column": "日期",
        "value_column": "库存",
        "source": "AKShare/Eastmoney:futures_inventory_em:cu",
        "period_type": "date",
        "symbol": "cu",
    },
    "COMEX_GOLD_INVENTORY": {
        "function": "futures_comex_inventory",
        "date_column": "日期",
        "value_column": "COMEX黄金库存量-吨",
        "source": "AKShare/Eastmoney:futures_comex_inventory:黄金",
        "period_type": "date",
        "symbol": "黄金",
    },
    "US_CRUDE_OIL_PRODUCTION": {
        "function": "macro_usa_crude_inner",
        "date_column": "日期",
        "value_column": "美国国内原油总量-产量",
        "source": "AKShare/Jin10:macro_usa_crude_inner",
        "period_type": "date",
    },
    "US_CRUDE_OIL_PRODUCTION_CHANGE": {
        "function": "macro_usa_crude_inner",
        "date_column": "日期",
        "value_column": "美国国内原油总量-变化",
        "source": "AKShare/Jin10:macro_usa_crude_inner",
        "period_type": "date",
    },
    "CN_GASOLINE_RETAIL_PRICE": {
        "function": "energy_oil_hist",
        "date_column": "调整日期",
        "value_column": "汽油价格",
        "source": "AKShare/Eastmoney:energy_oil_hist",
        "period_type": "date",
    },
    "CN_DIESEL_RETAIL_PRICE": {
        "function": "energy_oil_hist",
        "date_column": "调整日期",
        "value_column": "柴油价格",
        "source": "AKShare/Eastmoney:energy_oil_hist",
        "period_type": "date",
    },
    "BDTI_INDEX": {
        "function": "macro_china_bdti_index",
        "date_column": "日期",
        "value_column": "最新值",
        "source": "AKShare/Eastmoney:macro_china_bdti_index",
        "period_type": "date",
    },
    "BCTI_INDEX": {
        "function": "macro_shipping_bcti",
        "date_column": "日期",
        "value_column": "最新值",
        "source": "AKShare/Eastmoney:macro_shipping_bcti",
        "period_type": "date",
    },
    "BDI_INDEX": {
        "function": "macro_shipping_bdi",
        "date_column": "日期",
        "value_column": "最新值",
        "source": "AKShare/Eastmoney:macro_shipping_bdi",
        "period_type": "date",
    },
    "BCI_INDEX": {
        "function": "macro_shipping_bci",
        "date_column": "日期",
        "value_column": "最新值",
        "source": "AKShare/Eastmoney:macro_shipping_bci",
        "period_type": "date",
    },
    "BPI_INDEX": {
        "function": "macro_shipping_bpi",
        "date_column": "日期",
        "value_column": "最新值",
        "source": "AKShare/Eastmoney:macro_shipping_bpi",
        "period_type": "date",
    },
    "CN_SOCIETY_ELECTRICITY": {
        "function": "macro_china_society_electricity",
        "date_column": "统计时间",
        "value_column": "全社会用电量",
        "source": "AKShare/Sina:macro_china_society_electricity",
        "period_type": "decimal_month",
        "multiplier": "0.0001",
    },
    "CN_SOCIETY_ELECTRICITY_YOY": {
        "function": "macro_china_society_electricity",
        "date_column": "统计时间",
        "value_column": "全社会用电量同比",
        "source": "AKShare/Sina:macro_china_society_electricity",
        "period_type": "decimal_month",
    },
    "CN_ENERGY_INDEX": {
        "function": "macro_china_energy_index",
        "date_column": "日期",
        "value_column": "最新值",
        "source": "AKShare/Eastmoney:macro_china_energy_index",
        "period_type": "date",
    },
    "CN_MANUFACTURING_PMI": {
        "function": "macro_china_pmi",
        "date_column": "月份",
        "value_column": "制造业-指数",
        "source": "AKShare/Eastmoney:macro_china_pmi",
        "period_type": "month",
    },
    "CN_NON_MANUFACTURING_PMI": {
        "function": "macro_china_pmi",
        "date_column": "月份",
        "value_column": "非制造业-指数",
        "source": "AKShare/Eastmoney:macro_china_pmi",
        "period_type": "month",
    },
    "CN_CORPORATE_GOODS_PRICE_INDEX": {
        "function": "macro_china_qyspjg",
        "date_column": "月份",
        "value_column": "总指数-指数值",
        "source": "AKShare/Eastmoney:macro_china_qyspjg",
        "period_type": "month",
    },
    "US_ISM_MANUFACTURING_PMI": {
        "function": "macro_usa_ism_pmi",
        "date_column": "日期",
        "value_column": "今值",
        "source": "AKShare/Jin10:macro_usa_ism_pmi",
        "period_type": "date",
    },
    "US_UNEMPLOYMENT_RATE": {
        "function": "macro_usa_unemployment_rate",
        "date_column": "日期",
        "value_column": "今值",
        "source": "AKShare/Jin10:macro_usa_unemployment_rate",
        "period_type": "date",
    },
    "US_NONFARM_PAYROLLS": {
        "function": "macro_usa_non_farm",
        "date_column": "日期",
        "value_column": "今值",
        "source": "AKShare/Jin10:macro_usa_non_farm",
        "period_type": "date",
    },
    "US_CPI_YOY": {
        "function": "macro_usa_cpi_yoy",
        "date_column": "时间",
        "value_column": "现值",
        "source": "AKShare/Eastmoney:macro_usa_cpi_yoy",
        "period_type": "date",
    },
    "US_CORE_PCE_YOY": {
        "function": "macro_usa_core_pce_price",
        "date_column": "日期",
        "value_column": "今值",
        "source": "AKShare/Jin10:macro_usa_core_pce_price",
        "period_type": "date",
    },
    "US_RETAIL_SALES_MOM": {
        "function": "macro_usa_retail_sales",
        "date_column": "日期",
        "value_column": "今值",
        "source": "AKShare/Jin10:macro_usa_retail_sales",
        "period_type": "date",
    },
    "CN_TOTAL_SOCIAL_FINANCING": {
        "function": "macro_china_bank_financing",
        "date_column": "日期",
        "value_column": "最新值",
        "source": "AKShare/Eastmoney:macro_china_bank_financing",
        "period_type": "date",
    },
}

UNAVAILABLE_SERIES = {
    "CN_REAL_GDP": {
        "status": "blocked",
        "reason": "已尝试国家统计局 data.stats.gov.cn，当前环境返回 403。",
        "next_step": "配置 Wind，或改用可访问的国家统计局官方接口。",
    },
    "CN_MANUFACTURING_INVESTMENT": {
        "status": "pending_source",
        "reason": "尚未找到稳定返回制造业投资累计同比的公开接口。",
        "next_step": "接入国家统计局分项接口或 Wind。",
    },
    "CN_INFRASTRUCTURE_INVESTMENT": {
        "status": "pending_source",
        "reason": "尚未找到稳定返回基础设施投资累计同比的公开接口。",
        "next_step": "接入国家统计局分项接口或 Wind。",
    },
    "CN_REAL_ESTATE_INVESTMENT": {
        "status": "pending_source",
        "reason": "尚未找到稳定返回房地产开发投资累计同比的公开接口。",
        "next_step": "接入国家统计局房地产月度表或 Wind。",
    },
    "CN_PROPERTY_SALES_AREA": {
        "status": "pending_source",
        "reason": "尚未找到稳定返回商品房销售面积累计同比的公开接口。",
        "next_step": "接入国家统计局房地产月度表或 Wind。",
    },
    "CN_EXPORT_PRICE_INDEX": {
        "status": "pending_source",
        "reason": "尚未找到稳定返回海关出口价格指数的公开接口。",
        "next_step": "接入海关总署价格指数表或 Wind。",
    },
    "CN_IMPORT_PRICE_INDEX": {
        "status": "pending_source",
        "reason": "尚未找到稳定返回海关进口价格指数的公开接口。",
        "next_step": "接入海关总署价格指数表或 Wind。",
    },
    "US_EIA_CRUDE_STOCKS": {
        "status": "needs_key",
        "reason": "EIA 官方 API 需要 api_key，当前项目尚未配置可用密钥。",
        "next_step": "在 .env 中配置 EIA_API_KEY 后接入 EIA petroleum stocks 接口。",
    },
    "LME_COPPER_INVENTORY": {
        "status": "pending_source",
        "reason": "LME 库存数据需要稳定公开接口、授权数据源或 Wind。",
        "next_step": "确认 LME 授权接口、Wind 字段或可稳定下载的数据表。",
    },
    "SHFE_COPPER_INVENTORY": {
        "status": "pending_source",
        "reason": "上期所铜库存需要稳定解析交易所仓单或周库存表。",
        "next_step": "确认 SHFE 官方表格结构后接入解析器。",
    },
    "CN_XIAOBAODANG_MIXED_COAL_5500": {
        "status": "pending_source",
        "reason": "尚未找到稳定返回小保当 5500 大卡混煤历史价格的公开接口。",
        "next_step": "接入中国煤炭市场网数据库授权接口、矿方报价表或 Wind。",
    },
    "CN_HONGLIULIN_WASHED_MIDDLE_LUMP": {
        "status": "pending_source",
        "reason": "尚未找到稳定返回红柳林洗中块历史价格的公开接口。",
        "next_step": "接入中国煤炭市场网数据库授权接口、矿方报价表或 Wind。",
    },
    "US_API_CRUDE_STOCK_CHANGE": {
        "status": "pending_source",
        "reason": "AkShare/Jin10 美国 API 原油库存变动序列当前停更在 2025-09，不能作为当前监控源。",
        "next_step": "接入 API 官方授权源，或改用可持续更新的 EIA/FRED 口径。",
    },
    "US_EIA_CRUDE_STOCK_CHANGE": {
        "status": "pending_source",
        "reason": "AkShare/Jin10 美国 EIA 原油库存变动序列当前停更在 2025-09，不能作为当前监控源。",
        "next_step": "配置 EIA_API_KEY 后接入官方 EIA weekly petroleum status 口径。",
    },
    "TD3C_TANKER_FREIGHT": {
        "status": "pending_source",
        "reason": (
            "TD3C（中东 Gulf 至中国 VLCC）属于 Baltic Exchange 航线级油轮运价，"
            "未找到稳定免授权历史接口。"
        ),
        "next_step": (
            "接入 Baltic Exchange 授权数据、Clarksons/SSY/Braemar 授权源，"
            "或可审计内部油运数据库。"
        ),
    },
    "TD20_TANKER_FREIGHT": {
        "status": "pending_source",
        "reason": (
            "TD20（西非至欧洲 VLCC/Suezmax）属于 Baltic Exchange 航线级油轮运价，"
            "未找到稳定免授权历史接口。"
        ),
        "next_step": (
            "接入 Baltic Exchange 授权数据、Clarksons/SSY/Braemar 授权源，"
            "或可审计内部油运数据库。"
        ),
    },
    "TC2_TANKER_FREIGHT": {
        "status": "pending_source",
        "reason": (
            "TC2（欧洲至美东成品油轮）属于 Baltic Exchange 航线级油轮运价，"
            "未找到稳定免授权历史接口。"
        ),
        "next_step": (
            "接入 Baltic Exchange 授权数据、Clarksons/SSY/Braemar 授权源，"
            "或可审计内部油运数据库。"
        ),
    },
    "TC14_TANKER_FREIGHT": {
        "status": "pending_source",
        "reason": (
            "TC14（美湾至欧洲成品油轮）属于 Baltic Exchange 航线级油轮运价，"
            "未找到稳定免授权历史接口。"
        ),
        "next_step": (
            "接入 Baltic Exchange 授权数据、Clarksons/SSY/Braemar 授权源，"
            "或可审计内部油运数据库。"
        ),
    },
}

INDICATOR_AVAILABILITY = {
    **UNAVAILABLE_SERIES,
    "CN_DEBT_TO_GDP": {
        "status": "no_data",
        "reason": "World Bank 对中国中央政府债务占 GDP 指标当前可访问但无可写入观测值。",
        "next_step": "接入财政部、IMF、BIS 或 Wind 的政府债务口径。",
    },
    "CN_FISCAL_BALANCE_TO_GDP": {
        "status": "no_data",
        "reason": "World Bank 对中国财政余额占 GDP 指标当前可访问但无可写入观测值。",
        "next_step": "接入财政部财政收支口径、IMF 或 Wind。",
    },
}
