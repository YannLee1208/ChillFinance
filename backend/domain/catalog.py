"""宏观指标目录。"""

from backend.constant import FRED_TREASURY_SERIES
from backend.domain.models import IndicatorDefinition

_TREASURY_NAMES = {
    "US_DGS3MO": "U.S. Treasury 3M yield",
    "US_DGS2": "U.S. Treasury 2Y yield",
    "US_DGS5": "U.S. Treasury 5Y yield",
    "US_DGS10": "U.S. Treasury 10Y yield",
    "US_DGS30": "U.S. Treasury 30Y yield",
}

_SEED_INDICATORS = [
    IndicatorDefinition(
        code="CN_GDP_YOY",
        name="China GDP YoY",
        domain="country_macro",
        region="China",
        unit="%",
        frequency="quarterly",
        provider="seed",
        source="seed:country_macro",
        description="中国 GDP 同比增速，用于跟踪国内经济增长动能。",
        display_order=101,
    ),
    IndicatorDefinition(
        code="US_FISCAL_DEFICIT",
        name="U.S. fiscal deficit",
        domain="country_macro",
        region="United States",
        unit="USD bn",
        frequency="monthly",
        provider="seed",
        source="seed:country_macro",
        description="美国财政赤字月度指标，用于观察财政收支压力。",
        display_order=102,
    ),
    IndicatorDefinition(
        code="EU_DEBT_TO_GDP",
        name="Euro Area debt to GDP",
        domain="country_macro",
        region="Euro Area",
        unit="%",
        frequency="quarterly",
        provider="seed",
        source="seed:country_macro",
        description="欧元区政府债务占 GDP 比重，用于衡量债务负担。",
        display_order=103,
    ),
    IndicatorDefinition(
        code="JP_GDP_YOY",
        name="Japan GDP YoY",
        domain="country_macro",
        region="Japan",
        unit="%",
        frequency="quarterly",
        provider="seed",
        source="seed:country_macro",
        description="日本 GDP 同比增速，用于跟踪日本宏观景气变化。",
        display_order=104,
    ),
    IndicatorDefinition(
        code="CU_LME_INVENTORY",
        name="LME copper inventory",
        domain="nonferrous",
        region="Global",
        unit="tonne",
        frequency="daily",
        provider="seed",
        source="seed:nonferrous",
        description="LME 铜库存，用于观察有色金属供需边际变化。",
        display_order=201,
    ),
    IndicatorDefinition(
        code="OIL_BRENT_PRICE",
        name="Brent crude oil price",
        domain="crude_oil",
        region="Global",
        unit="USD/bbl",
        frequency="daily",
        provider="seed",
        source="seed:crude_oil",
        description="布伦特原油价格，用于跟踪全球原油市场定价。",
        display_order=301,
    ),
    IndicatorDefinition(
        code="COAL_QHD_PRICE",
        name="Qinhuangdao coal price",
        domain="coal",
        region="China",
        unit="CNY/tonne",
        frequency="weekly",
        provider="seed",
        source="seed:coal",
        description="秦皇岛煤炭价格，用于观察国内动力煤市场变化。",
        display_order=401,
    ),
    IndicatorDefinition(
        code="CN_POWER_GENERATION",
        name="China power generation",
        domain="power",
        region="China",
        unit="TWh",
        frequency="monthly",
        provider="seed",
        source="seed:power",
        description="中国发电量，用于衡量实体经济用电需求。",
        display_order=501,
    ),
]


def _treasury_indicators() -> list[IndicatorDefinition]:
    """生成 FRED 美国国债收益率指标定义。"""

    indicators: list[IndicatorDefinition] = []
    for display_order, (code, fred_code) in enumerate(FRED_TREASURY_SERIES.items(), start=1):
        indicators.append(
            IndicatorDefinition(
                code=code,
                name=_TREASURY_NAMES[code],
                domain="rates",
                region="United States",
                unit="%",
                frequency="daily",
                provider="fred",
                source=f"FRED:{fred_code}",
                description="美国国债收益率，用于观察美元利率曲线和市场风险偏好。",
                display_order=display_order,
            )
        )
    return indicators


def get_catalog() -> list[IndicatorDefinition]:
    """返回按展示顺序排序的指标目录。"""

    return sorted([*_treasury_indicators(), *_SEED_INDICATORS], key=lambda item: item.display_order)


def get_indicator(code: str) -> IndicatorDefinition:
    """按指标代码返回指标定义。"""

    for indicator in get_catalog():
        if indicator.code == code:
            return indicator
    raise KeyError(f"Unknown indicator code: {code}")
