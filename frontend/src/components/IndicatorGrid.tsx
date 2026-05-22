import { useQueries } from "@tanstack/react-query";

import { fetchIndicatorSnapshot } from "../api";
import type { IndicatorDefinition } from "../types";
import { IndicatorCard } from "./IndicatorCard";
import type { TimeRangeKey } from "./timeRange";

type IndicatorGridProps = {
  indicators: IndicatorDefinition[];
  timeRange: TimeRangeKey;
};

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

  return (
    <section className="indicator-grid">
      {results.map((result) =>
        result.data ? (
          <IndicatorCard
            key={result.data.definition.code}
            snapshot={result.data}
            timeRange={timeRange}
          />
        ) : null,
      )}
    </section>
  );
}
