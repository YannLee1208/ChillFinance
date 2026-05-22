import type { IndicatorDefinition, Observation } from "../types";

export type LocalizedIndicator = {
  name: string;
  description: string;
  unit: string;
  sourceLabel: string;
};

const wb = "世界银行";
const fred = "FRED";
const akEastmoney = "AkShare / 东方财富";
const akMarket = "AkShare / 行情源";
const pendingNbsWind = "国家统计局 / Wind 待接入";
const pendingPbocWind = "人民银行 / Wind 待接入";
const pendingCustomsWind = "海关总署 / Wind 待接入";

const INDICATOR_LABELS: Record<string, LocalizedIndicator> = {
  US_DGS3MO: {
    name: "美国国债收益率 3M",
    description: "美国财政部官方日频国债收益率，短端主要反映政策利率路径和流动性预期。",
    unit: "%",
    sourceLabel: "美国财政部",
  },
  US_DGS2: {
    name: "美国国债收益率 2Y",
    description: "美国财政部官方日频国债收益率，2年期对货币政策预期更敏感。",
    unit: "%",
    sourceLabel: "美国财政部",
  },
  US_DGS5: {
    name: "美国国债收益率 5Y",
    description: "美国财政部官方日频国债收益率，适合观察中端实际利率和增长预期。",
    unit: "%",
    sourceLabel: "美国财政部",
  },
  US_DGS10: {
    name: "美国国债收益率 10Y",
    description: "美国财政部官方日频国债收益率，长端定价通胀、增长和期限溢价。",
    unit: "%",
    sourceLabel: "美国财政部",
  },
  US_DGS30: {
    name: "美国国债收益率 30Y",
    description: "美国财政部官方日频国债收益率，超长端用于观察期限溢价和财政供给压力。",
    unit: "%",
    sourceLabel: "美国财政部",
  },
  JP_LONG_RATE: { name: "日本长期国债收益率", description: "用于横向比较主要经济体长端利率。", unit: "%", sourceLabel: fred },
  DE_LONG_RATE: { name: "德国长期国债收益率", description: "用于观察欧洲核心利率变化。", unit: "%", sourceLabel: fred },
  EU_LONG_RATE: { name: "欧元区长期国债收益率", description: "用于观察欧洲整体长端利率。", unit: "%", sourceLabel: fred },
  US_GDP: { name: "美国名义 GDP", description: "衡量美国经济总量和周期趋势。", unit: "十亿美元", sourceLabel: fred },
  US_FEDERAL_DEBT: { name: "美国联邦债务规模", description: "用于观察美国财政杠杆。", unit: "百万美元", sourceLabel: fred },
  US_DEBT_TO_GDP: { name: "美国联邦债务 / GDP", description: "用于衡量债务负担。", unit: "%", sourceLabel: fred },
  US_FISCAL_BALANCE_TO_GDP: { name: "美国财政余额 / GDP", description: "负值代表财政赤字。", unit: "%", sourceLabel: fred },
  CN_GDP: { name: "中国名义 GDP（美元口径）", description: "世界银行年度现价美元 GDP。", unit: "美元", sourceLabel: wb },
  CN_NOMINAL_GDP_QUARTERLY: { name: "中国名义 GDP", description: "国家统计口径季度累计现价 GDP。", unit: "亿元", sourceLabel: akEastmoney },
  CN_REAL_GDP: { name: "中国实际 GDP", description: "需要国家统计局不变价序列或 Wind 接入，当前不写入模拟值。", unit: "指数 / 人民币", sourceLabel: pendingNbsWind },
  CN_REAL_GDP_GROWTH: { name: "中国实际 GDP 增速（年度）", description: "用于观察经济总量的真实增长。", unit: "%", sourceLabel: wb },
  CN_REAL_GDP_QUARTERLY_YOY: { name: "中国实际 GDP 增速", description: "GDP 不变价同比增速，用于观察实际增长。", unit: "%", sourceLabel: akEastmoney },
  CN_HOUSEHOLD_CONSUMPTION: { name: "居民最终消费支出", description: "用于观察消费对总需求的贡献。", unit: "美元", sourceLabel: wb },
  CN_RETAIL_SALES: { name: "社会消费品零售总额同比", description: "社零是国内消费修复的核心月度指标。", unit: "%", sourceLabel: akEastmoney },
  CN_GROSS_CAPITAL_FORMATION: { name: "资本形成总额", description: "用于观察投资和库存变动形成的需求。", unit: "美元", sourceLabel: wb },
  CN_INDUSTRY_VALUE_ADDED: { name: "工业增加值（年度）", description: "用于观察工业部门产出规模。", unit: "美元", sourceLabel: wb },
  CN_INDUSTRIAL_PRODUCTION_YOY: { name: "规模以上工业增加值同比", description: "用于跟踪工业生产景气。", unit: "%", sourceLabel: akEastmoney },
  CN_FIXED_ASSET_INVESTMENT: { name: "固定资产投资同比", description: "用于观察投资需求。", unit: "%", sourceLabel: akEastmoney },
  CN_MANUFACTURING_INVESTMENT: { name: "制造业投资", description: "制造业投资累计同比仍需稳定官方接口或 Wind。", unit: "%", sourceLabel: pendingNbsWind },
  CN_INFRASTRUCTURE_INVESTMENT: { name: "基建投资", description: "基建投资累计同比仍需稳定官方接口或 Wind。", unit: "%", sourceLabel: pendingNbsWind },
  CN_REAL_ESTATE_INVESTMENT: { name: "房地产开发投资", description: "房地产开发投资累计同比仍需稳定官方接口或 Wind。", unit: "%", sourceLabel: pendingNbsWind },
  CN_PROPERTY_SALES_AREA: { name: "商品房销售面积", description: "商品房销售面积累计同比仍需稳定官方接口或 Wind。", unit: "%", sourceLabel: pendingNbsWind },
  CN_NEW_HOME_PRICE_INDEX: { name: "新建商品住宅价格指数", description: "新房价格样本均值，用于观察房价变化。", unit: "指数", sourceLabel: akEastmoney },
  CN_EXPORTS_GOODS_SERVICES: { name: "货物和服务出口额", description: "用于观察外需和贸易景气。", unit: "美元", sourceLabel: wb },
  CN_IMPORTS_GOODS_SERVICES: { name: "货物和服务进口额", description: "用于观察内需和补库变化。", unit: "美元", sourceLabel: wb },
  CN_EXPORT_YOY_USD: { name: "出口同比（美元）", description: "以美元计出口同比，用于观察外需变化。", unit: "%", sourceLabel: "AkShare / Jin10" },
  CN_IMPORT_YOY_USD: { name: "进口同比（美元）", description: "以美元计进口同比，用于观察内需和补库变化。", unit: "%", sourceLabel: "AkShare / Jin10" },
  CN_CPI_INFLATION: { name: "CPI 通胀率", description: "年度 CPI 通胀率，用于观察居民端价格压力。", unit: "%", sourceLabel: wb },
  CN_PPI: { name: "PPI 同比", description: "用于观察工业品出厂价格和企业盈利压力。", unit: "%", sourceLabel: akEastmoney },
  CN_EXPORT_PRICE_INDEX: { name: "出口价格指数", description: "出口价格指数仍需海关总署稳定接口或 Wind。", unit: "指数", sourceLabel: pendingCustomsWind },
  CN_IMPORT_PRICE_INDEX: { name: "进口价格指数", description: "进口价格指数仍需海关总署稳定接口或 Wind。", unit: "指数", sourceLabel: pendingCustomsWind },
  CN_TOTAL_SOCIAL_FINANCING: { name: "社会融资规模", description: "社会融资规模月度值，用于观察实体经济融资需求。", unit: "亿元", sourceLabel: akEastmoney },
  CN_RMB_LOANS: { name: "新增人民币贷款", description: "新增信贷当月值，用于观察信用投放强弱。", unit: "亿元", sourceLabel: akEastmoney },
  CN_M2: { name: "中国 M2", description: "广义货币供应量，反映总量流动性。", unit: "亿元", sourceLabel: akEastmoney },
  CN_M2_YOY: { name: "中国 M2 同比", description: "广义货币供应量同比增速，反映总量流动性扩张速度。", unit: "%", sourceLabel: akEastmoney },
  CN_M1: { name: "中国 M1", description: "狭义货币供应量，用于观察企业活期资金和交易活跃度。", unit: "亿元", sourceLabel: akEastmoney },
  CN_M1_YOY: { name: "中国 M1 同比", description: "狭义货币供应量同比增速，用于观察资金活化变化。", unit: "%", sourceLabel: akEastmoney },
  CN_M0: { name: "中国 M0", description: "流通中现金，用于观察现金需求。", unit: "亿元", sourceLabel: akEastmoney },
  CN_M0_YOY: { name: "中国 M0 同比", description: "流通中现金同比增速。", unit: "%", sourceLabel: akEastmoney },
  CN_M1_M2_SCISSORS: { name: "M1-M2 剪刀差", description: "M1 同比减 M2 同比，用于观察资金活化程度。", unit: "百分点", sourceLabel: akEastmoney },
  CN_OFFICIAL_EXCHANGE_RATE: { name: "人民币兑美元官方平均汇率", description: "年度官方平均汇率。", unit: "人民币/美元", sourceLabel: wb },
  CN_SHCOMP: { name: "上证综指", description: "用于观察国内金融市场风险偏好。", unit: "指数", sourceLabel: akMarket },
  US_EIA_CRUDE_STOCKS: { name: "美国商业原油库存", description: "EIA 周度原油库存，需要配置 EIA API Key 后接入。", unit: "千桶", sourceLabel: "EIA 待接入" },
  LME_COPPER_INVENTORY: { name: "LME 铜库存", description: "海外铜显性库存，需要 LME 授权接口、Wind 或稳定数据表。", unit: "吨", sourceLabel: "LME / Wind 待接入" },
  SHFE_COPPER_INVENTORY: { name: "上期所铜库存", description: "国内铜显性库存，需要稳定解析 SHFE 官方库存表。", unit: "吨", sourceLabel: "SHFE / Wind 待接入" },
  JP_GDP: { name: "日本名义 GDP", description: "日本现价美元 GDP。", unit: "美元", sourceLabel: wb },
  EU_GDP: { name: "欧元区名义 GDP", description: "欧元区现价美元 GDP。", unit: "美元", sourceLabel: wb },
  CN_DEBT_TO_GDP: { name: "中国政府债务 / GDP", description: "用于观察财政杠杆。", unit: "%", sourceLabel: wb },
  JP_DEBT_TO_GDP: { name: "日本政府债务 / GDP", description: "用于观察债务负担。", unit: "%", sourceLabel: wb },
  EU_DEBT_TO_GDP: { name: "欧元区政府债务 / GDP", description: "用于观察债务负担。", unit: "%", sourceLabel: wb },
  CN_FISCAL_BALANCE_TO_GDP: { name: "中国财政余额 / GDP", description: "负值代表财政赤字。", unit: "%", sourceLabel: wb },
  JP_FISCAL_BALANCE_TO_GDP: { name: "日本财政余额 / GDP", description: "负值代表财政赤字。", unit: "%", sourceLabel: wb },
  EU_FISCAL_BALANCE_TO_GDP: { name: "欧元区财政余额 / GDP", description: "负值代表财政赤字。", unit: "%", sourceLabel: wb },
  CU_PRICE: { name: "铜价", description: "全球铜价，用于观察工业需求和制造业景气。", unit: "美元/吨", sourceLabel: fred },
  AL_PRICE: { name: "铝价", description: "全球铝价，用于观察轻金属供需。", unit: "美元/吨", sourceLabel: fred },
  NI_PRICE: { name: "镍价", description: "全球镍价，用于跟踪不锈钢和新能源材料链。", unit: "美元/吨", sourceLabel: fred },
  ZN_PRICE: { name: "锌价", description: "全球锌价，用于观察镀锌和基建需求。", unit: "美元/吨", sourceLabel: fred },
  PB_PRICE: { name: "铅价", description: "全球铅价，用于观察蓄电池和工业需求。", unit: "美元/吨", sourceLabel: fred },
  IRON_ORE_PRICE: { name: "铁矿石价格", description: "用于观察黑色链条和工业原料需求。", unit: "美元/干吨", sourceLabel: fred },
  OIL_BRENT_PRICE: { name: "Brent 原油", description: "Brent 现货价格，用于观察全球原油定价。", unit: "美元/桶", sourceLabel: fred },
  OIL_WTI_PRICE: { name: "WTI 原油", description: "WTI 现货价格，用于观察美国原油定价。", unit: "美元/桶", sourceLabel: fred },
  US_GASOLINE_PRICE: { name: "美国汽油零售价", description: "用于观察成品油终端价格。", unit: "美元/加仑", sourceLabel: fred },
  EU_NATURAL_GAS_PRICE: { name: "欧洲天然气价格", description: "用于观察能源链价格压力。", unit: "美元/MMBtu", sourceLabel: fred },
  COAL_AUSTRALIA_PRICE: { name: "澳洲动力煤价格", description: "用于观察海运动力煤基准变化。", unit: "美元/吨", sourceLabel: fred },
  US_POWER_PRODUCTION: { name: "美国电力生产指数", description: "用于观察电力需求和工业活动。", unit: "指数", sourceLabel: fred },
};

const SELECTOR_VALUE_LABELS: Record<string, string> = {
  "United States": "美国",
  Japan: "日本",
  Germany: "德国",
  "Euro Area": "欧元区",
  China: "中国",
  Global: "全球",
  Europe: "欧洲",
  Yield: "收益率",
  GDP: "名义 GDP",
  Debt: "债务规模",
  "Debt/GDP": "债务/GDP",
  "Fiscal balance": "财政余额",
  Price: "价格",
  "Crude price": "原油价格",
  "Product price": "成品油价格",
  "Gas price": "天然气价格",
  Production: "生产指数",
  Copper: "铜",
  Aluminum: "铝",
  Nickel: "镍",
  Zinc: "锌",
  Lead: "铅",
  "Iron ore": "铁矿石",
  Inventory: "库存",
  "Crude oil": "原油",
  LME: "LME",
  SHFE: "上期所",
  Brent: "Brent",
  WTI: "WTI",
  Gasoline: "汽油",
  "Natural gas": "天然气",
  "Thermal coal": "动力煤",
  "Long-term": "长期",
};

export function localizeIndicator(definition: IndicatorDefinition): LocalizedIndicator {
  return (
    INDICATOR_LABELS[definition.code] ?? {
      name: definition.name,
      description: definition.description,
      unit: definition.unit,
      sourceLabel: definition.provider,
    }
  );
}

export function localizeIndicatorCode(code: string): string {
  return INDICATOR_LABELS[code]?.name ?? code;
}

export function localizeSelectorValue(value: string): string {
  return SELECTOR_VALUE_LABELS[value] ?? value;
}

export function selectorSummary(definition: IndicatorDefinition): string {
  return Object.values(definition.selectors).map(localizeSelectorValue).join(" / ") || definition.region;
}

export function latestInRange(points: Observation[]): Observation | null {
  return points.length > 0 ? points[points.length - 1] : null;
}
