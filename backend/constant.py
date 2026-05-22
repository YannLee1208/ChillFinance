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
}
