import { useQueries } from "@tanstack/react-query";

import { fetchIndicatorSnapshot } from "../api";
import type { IndicatorDefinition, IndicatorSnapshot } from "../types";
import { IndicatorCard } from "./IndicatorCard";
import { localizeIndicator } from "./localization";
import type { TimeRangeKey } from "./timeRange";

type IndicatorGridProps = {
  indicators: IndicatorDefinition[];
  timeRange: TimeRangeKey;
};

const AVAILABILITY_LABELS: Record<string, string> = {
  available: "可更新",
  pending_source: "待接入数据源",
  needs_key: "需要密钥",
  blocked: "当前受阻",
  no_data: "暂无返回",
};

function availabilityText(indicator: IndicatorDefinition, fallbackDescription: string): string {
  const availability = indicator.availability;
  if (!availability || availability.status === "available") {
    return fallbackDescription;
  }
  return [availability.reason, availability.next_step ? `下一步：${availability.next_step}` : ""]
    .filter(Boolean)
    .join(" ");
}

export function IndicatorGrid({ indicators, timeRange }: IndicatorGridProps) {
  const results = useQueries({
    queries: indicators.map((indicator) => ({
      queryKey: ["indicator", indicator.code],
      queryFn: () => fetchIndicatorSnapshot(indicator.code),
    })),
  });

  if (indicators.length === 0) {
    return <section className="state-panel compact">当前主题暂无指标</section>;
  }

  if (results.some((result) => result.isLoading)) {
    return <section className="state-panel compact">正在加载指标快照</section>;
  }

  if (results.some((result) => result.isError)) {
    return <section className="state-panel compact">指标快照加载失败</section>;
  }

  const snapshots = results
    .map((result) => result.data)
    .filter((snapshot): snapshot is IndicatorSnapshot => Boolean(snapshot));
  const availableSnapshots = snapshots.filter((snapshot) => snapshot.points.length > 0);
  const unavailableSnapshots = snapshots.filter((snapshot) => snapshot.points.length === 0);

  return (
    <>
      {availableSnapshots.length > 0 ? (
        <section className="indicator-grid">
          {availableSnapshots.map((snapshot) => (
            <IndicatorCard
              key={snapshot.definition.code}
              snapshot={snapshot}
              timeRange={timeRange}
            />
          ))}
        </section>
      ) : (
        <section className="state-panel compact">当前筛选下暂无已入库的真实序列。</section>
      )}
      {unavailableSnapshots.length > 0 ? (
        <section className="pending-panel">
          <div className="pending-head">
            <span>待接入 / 暂无返回</span>
            <strong>{unavailableSnapshots.length} 个指标未展示为空图</strong>
          </div>
          <div className="pending-list">
            {unavailableSnapshots.map((snapshot) => {
              const localized = localizeIndicator(snapshot.definition);
              return (
                <article key={snapshot.definition.code}>
                  <b>{localized.name}</b>
                  <p>{availabilityText(snapshot.definition, localized.description)}</p>
                  <span>
                    {AVAILABILITY_LABELS[snapshot.definition.availability.status] ?? "待确认"} ·{" "}
                    {localized.sourceLabel}
                  </span>
                </article>
              );
            })}
          </div>
        </section>
      ) : null}
    </>
  );
}
