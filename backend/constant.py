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

UNAVAILABLE_SERIES = {
    "CN_REAL_GDP": (
        "已尝试国家统计局 data.stats.gov.cn，当前环境返回 403；"
        "需要 Wind 或可访问的官方统计局接口。"
    ),
    "CN_TOTAL_SOCIAL_FINANCING": (
        "需要接入人民银行社会融资规模月度表或 Wind 宏观数据库；"
        "当前没有稳定官方 JSON 接口。"
    ),
    "CN_RMB_LOANS": (
        "需要接入人民银行人民币贷款月度表或 Wind 宏观数据库；"
        "当前没有稳定官方 JSON 接口。"
    ),
    "CN_M1": "需要接入人民银行 M1 月度表或 Wind 宏观数据库；当前没有稳定官方 JSON 接口。",
    "CN_M1_M2_SCISSORS": "需要先接入真实 M1 和 M2 后计算 M1-M2 剪刀差；当前不会用模拟值替代。",
    "CN_RETAIL_SALES": "需要接入国家统计局社会消费品零售总额月度序列或 Wind。",
    "CN_INDUSTRIAL_PRODUCTION_YOY": "需要接入国家统计局规模以上工业增加值月度同比或 Wind。",
    "CN_FIXED_ASSET_INVESTMENT": "需要接入国家统计局固定资产投资累计同比或 Wind。",
    "CN_MANUFACTURING_INVESTMENT": "需要接入制造业投资累计同比或 Wind。",
    "CN_INFRASTRUCTURE_INVESTMENT": "需要接入基础设施投资累计同比或 Wind。",
    "CN_REAL_ESTATE_INVESTMENT": "需要接入国家统计局房地产开发投资累计同比或 Wind。",
    "CN_PROPERTY_SALES_AREA": "需要接入商品房销售面积累计同比或 Wind。",
    "CN_NEW_HOME_PRICE_INDEX": "需要接入70城新建商品住宅价格指数或 Wind。",
    "CN_PPI": "需要接入国家统计局工业生产者出厂价格指数 PPI 或 Wind。",
    "CN_EXPORT_PRICE_INDEX": "需要接入海关总署出口价格指数或 Wind。",
    "CN_IMPORT_PRICE_INDEX": "需要接入海关总署进口价格指数或 Wind。",
    "CN_SHCOMP": "需要接入交易所/行情源的上证综指或 Wind。",
}
