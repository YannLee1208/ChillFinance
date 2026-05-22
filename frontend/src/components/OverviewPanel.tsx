import type { IndicatorDefinition } from "../types";
import { DOMAIN_LABELS } from "./DomainSidebar";

type OverviewPanelProps = {
  activeDomain: string;
  indicators: IndicatorDefinition[];
};

export function OverviewPanel({ activeDomain, indicators }: OverviewPanelProps) {
  const label = DOMAIN_LABELS[activeDomain] ?? { title: activeDomain, subtitle: "扩展指标" };
  const providers = Array.from(new Set(indicators.map((indicator) => indicator.provider))).join(" / ");
  const frequencies = Array.from(new Set(indicators.map((indicator) => indicator.frequency))).join(" / ");
  const regions = Array.from(new Set(indicators.map((indicator) => indicator.region)));

  return (
    <section className="overview-panel">
      <div className="overview-title">
        <div>
          <span>{label.subtitle}</span>
          <h2>{label.title}</h2>
        </div>
        <strong>{indicators.length}</strong>
      </div>
      <div className="overview-stats">
        <div>
          <span>数据源</span>
          <b>{providers || "--"}</b>
        </div>
        <div>
          <span>频率</span>
          <b>{frequencies || "--"}</b>
        </div>
        <div>
          <span>地区</span>
          <b>{regions.length ? regions.slice(0, 3).join(" / ") : "--"}</b>
        </div>
      </div>
    </section>
  );
}
