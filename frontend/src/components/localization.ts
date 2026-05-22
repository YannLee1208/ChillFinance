import type { IndicatorDefinition, Observation } from "../types";

export type LocalizedIndicator = {
  name: string;
  description: string;
  unit: string;
  sourceLabel: string;
};

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
  JP_LONG_RATE: {
    name: "日本长期国债收益率",
    description: "日本长期政府债券收益率，用于横向比较主要经济体长端利率。",
    unit: "%",
    sourceLabel: "FRED",
  },
  DE_LONG_RATE: {
    name: "德国长期国债收益率",
    description: "德国长期政府债券收益率，用于观察欧洲核心利率变化。",
    unit: "%",
    sourceLabel: "FRED",
  },
  EU_LONG_RATE: {
    name: "欧元区长期国债收益率",
    description: "欧元区长期政府债券收益率，用于观察欧洲整体长端利率。",
    unit: "%",
    sourceLabel: "FRED",
  },
  US_GDP: {
    name: "美国名义 GDP",
    description: "美国名义 GDP，衡量经济总量和周期趋势。",
    unit: "十亿美元",
    sourceLabel: "FRED",
  },
  US_FEDERAL_DEBT: {
    name: "美国联邦债务规模",
    description: "美国联邦政府债务余额，用于观察财政杠杆。",
    unit: "百万美元",
    sourceLabel: "FRED",
  },
  US_DEBT_TO_GDP: {
    name: "美国联邦债务 / GDP",
    description: "美国联邦债务占 GDP 比重，用于衡量债务负担。",
    unit: "%",
    sourceLabel: "FRED",
  },
  US_FISCAL_BALANCE_TO_GDP: {
    name: "美国财政余额 / GDP",
    description: "财政余额占 GDP 比重，负值代表财政赤字。",
    unit: "%",
    sourceLabel: "FRED",
  },
  CN_REAL_GDP: {
    name: "中国实际 GDP",
    description: "实际 GDP 需要国家统计局不变价序列或 Wind 接入；当前不展示模拟值。",
    unit: "指数/人民币",
    sourceLabel: "国家统计局/Wind 待接入",
  },
  CN_GDP: {
    name: "中国名义 GDP",
    description: "中国现价美元 GDP，用于观察经济总量变化。",
    unit: "美元",
    sourceLabel: "世界银行",
  },
  CN_TOTAL_SOCIAL_FINANCING: {
    name: "社会融资规模",
    description: "社融需要人民银行官方表或 Wind 接入；当前不展示模拟值。",
    unit: "亿元",
    sourceLabel: "人民银行/Wind 待接入",
  },
  CN_RMB_LOANS: {
    name: "人民币贷款",
    description: "人民币贷款需要人民银行官方表或 Wind 接入；当前不展示模拟值。",
    unit: "亿元",
    sourceLabel: "人民银行/Wind 待接入",
  },
  CN_M2: {
    name: "中国 M2",
    description: "广义货币供应量 M2，反映银行体系存款和流动性扩张。",
    unit: "亿元",
    sourceLabel: "ChinaData.live / PBOC 口径",
  },
  CN_M1: {
    name: "中国 M1",
    description: "狭义货币供应量 M1 需要人民银行官方表或 Wind 接入；当前不展示模拟值。",
    unit: "亿元",
    sourceLabel: "人民银行/Wind 待接入",
  },
  CN_M1_M2_SCISSORS: {
    name: "M1-M2 剪刀差",
    description: "M1-M2 剪刀差用于观察企业活化资金和信用传导，需真实 M1 与 M2 后计算。",
    unit: "百分点",
    sourceLabel: "人民银行/Wind 待接入",
  },
  CU_PRICE: { name: "铜价", description: "全球铜价，用于观察工业需求和制造业景气。", unit: "美元/吨", sourceLabel: "FRED" },
  AL_PRICE: { name: "铝价", description: "全球铝价，用于观察轻金属供需。", unit: "美元/吨", sourceLabel: "FRED" },
  NI_PRICE: { name: "镍价", description: "全球镍价，用于跟踪不锈钢和新能源材料链。", unit: "美元/吨", sourceLabel: "FRED" },
  ZN_PRICE: { name: "锌价", description: "全球锌价，用于观察镀锌和基建需求。", unit: "美元/吨", sourceLabel: "FRED" },
  PB_PRICE: { name: "铅价", description: "全球铅价，用于观察蓄电池和工业需求。", unit: "美元/吨", sourceLabel: "FRED" },
  IRON_ORE_PRICE: { name: "铁矿石价格", description: "铁矿石价格，用于观察黑色链条和工业原料需求。", unit: "美元/干吨", sourceLabel: "FRED" },
  OIL_BRENT_PRICE: { name: "Brent 原油", description: "Brent 现货价格，用于观察全球原油定价。", unit: "美元/桶", sourceLabel: "FRED" },
  OIL_WTI_PRICE: { name: "WTI 原油", description: "WTI 现货价格，用于观察美国原油定价。", unit: "美元/桶", sourceLabel: "FRED" },
  US_GASOLINE_PRICE: { name: "美国汽油零售价", description: "美国普通汽油零售价格，用于观察成品油终端价格。", unit: "美元/加仑", sourceLabel: "FRED" },
  EU_NATURAL_GAS_PRICE: { name: "欧洲天然气价格", description: "欧洲天然气价格，用于观察能源链价格压力。", unit: "美元/MMBtu", sourceLabel: "FRED" },
  COAL_AUSTRALIA_PRICE: { name: "澳洲动力煤价格", description: "澳洲煤炭价格，用于观察海运动力煤基准变化。", unit: "美元/吨", sourceLabel: "FRED" },
  US_POWER_PRODUCTION: { name: "美国电力生产指数", description: "美国电力生产指数，用于观察电力需求和工业活动。", unit: "指数", sourceLabel: "FRED" },
  JP_GDP: { name: "日本名义 GDP", description: "日本现价美元 GDP，用于观察经济总量变化。", unit: "美元", sourceLabel: "世界银行" },
  EU_GDP: { name: "欧元区名义 GDP", description: "欧元区现价美元 GDP，用于观察经济总量变化。", unit: "美元", sourceLabel: "世界银行" },
  CN_DEBT_TO_GDP: { name: "中国政府债务 / GDP", description: "政府债务占 GDP 比重，用于观察财政杠杆。", unit: "%", sourceLabel: "世界银行" },
  JP_DEBT_TO_GDP: { name: "日本政府债务 / GDP", description: "政府债务占 GDP 比重，用于观察债务负担。", unit: "%", sourceLabel: "世界银行" },
  EU_DEBT_TO_GDP: { name: "欧元区政府债务 / GDP", description: "政府债务占 GDP 比重，用于观察债务负担。", unit: "%", sourceLabel: "世界银行" },
  CN_FISCAL_BALANCE_TO_GDP: { name: "中国财政余额 / GDP", description: "财政余额占 GDP 比重，负值代表财政赤字。", unit: "%", sourceLabel: "世界银行" },
  JP_FISCAL_BALANCE_TO_GDP: { name: "日本财政余额 / GDP", description: "财政余额占 GDP 比重，负值代表财政赤字。", unit: "%", sourceLabel: "世界银行" },
  EU_FISCAL_BALANCE_TO_GDP: { name: "欧元区财政余额 / GDP", description: "财政余额占 GDP 比重，负值代表财政赤字。", unit: "%", sourceLabel: "世界银行" },
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
  "Real GDP": "实际 GDP",
  Debt: "债务规模",
  "Debt/GDP": "债务/GDP",
  "Fiscal balance": "财政余额",
  "Social financing": "社会融资规模",
  "RMB loans": "人民币贷款",
  "M1-M2 scissors": "M1-M2 剪刀差",
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

export function localizeSelectorValue(value: string): string {
  return SELECTOR_VALUE_LABELS[value] ?? value;
}

export function selectorSummary(definition: IndicatorDefinition): string {
  return Object.values(definition.selectors).map(localizeSelectorValue).join(" / ") || definition.region;
}

export function latestInRange(points: Observation[]): Observation | null {
  return points.length > 0 ? points[points.length - 1] : null;
}
