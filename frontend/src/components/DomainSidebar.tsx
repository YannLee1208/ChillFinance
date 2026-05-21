import type { IndicatorDefinition } from "../types";

export const DOMAIN_LABELS: Record<string, { title: string; subtitle: string }> = {
  rates: { title: "国债利率", subtitle: "期限 / 曲线" },
  country_macro: { title: "各国经济", subtitle: "GDP / 财政 / 债务" },
  nonferrous: { title: "有色板块", subtitle: "金银铜铝 / 库存" },
  crude_oil: { title: "原油板块", subtitle: "原油 / 成品油 / 油运" },
  coal: { title: "煤炭板块", subtitle: "价格 / 库存 / 产能" },
  power: { title: "电力板块", subtitle: "发电 / 用电 / 电煤" },
};

const DOMAIN_ORDER = ["rates", "country_macro", "nonferrous", "crude_oil", "coal", "power"];

type DomainSidebarProps = {
  catalog: IndicatorDefinition[];
  activeDomain: string;
  onSelectDomain: (domain: string) => void;
};

export function DomainSidebar({ catalog, activeDomain, onSelectDomain }: DomainSidebarProps) {
  const domainCounts = catalog.reduce<Record<string, number>>((counts, indicator) => {
    counts[indicator.domain] = (counts[indicator.domain] ?? 0) + 1;
    return counts;
  }, {});
  const domains = DOMAIN_ORDER.filter((domain) => domainCounts[domain]);

  return (
    <aside className="sidebar">
      {domains.map((domain) => {
        const label = DOMAIN_LABELS[domain];
        const isActive = domain === activeDomain;
        return (
          <button
            className={isActive ? "nav-item active" : "nav-item"}
            key={domain}
            onClick={() => onSelectDomain(domain)}
            type="button"
          >
            <span className="nav-title">{label.title}</span>
            <span className="nav-subtitle">{label.subtitle}</span>
            <span className="nav-count">{domainCounts[domain]}</span>
          </button>
        );
      })}
    </aside>
  );
}
