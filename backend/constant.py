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
    "CN_M1": {
        "function": "macro_china_money_supply",
        "date_column": "月份",
        "value_column": "货币(M1)-数量(亿元)",
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
    "CN_EXPORT_YOY_USD": {
        "function": "macro_china_exports_yoy",
        "date_column": "日期",
        "value_column": "今值",
        "source": "AKShare/Jin10:macro_china_exports_yoy",
        "period_type": "date",
    },
    "CN_IMPORT_YOY_USD": {
        "function": "macro_china_imports_yoy",
        "date_column": "日期",
        "value_column": "今值",
        "source": "AKShare/Jin10:macro_china_imports_yoy",
        "period_type": "date",
    },
    "CN_SHCOMP": {
        "function": "stock_zh_index_daily",
        "date_column": "date",
        "value_column": "close",
        "source": "AKShare/Sina:stock_zh_index_daily:sh000001",
        "period_type": "date",
        "symbol": "sh000001",
    },
}

UNAVAILABLE_SERIES = {
    "CN_REAL_GDP": {
        "status": "blocked",
        "reason": "已尝试国家统计局 data.stats.gov.cn，当前环境返回 403。",
        "next_step": "配置 Wind，或改用可访问的国家统计局官方接口。",
    },
    "CN_TOTAL_SOCIAL_FINANCING": {
        "status": "pending_source",
        "reason": "当前没有稳定官方 JSON 接口可直接拉取人民银行社会融资规模月度表。",
        "next_step": "接入人民银行表格解析或 Wind 宏观数据库。",
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
