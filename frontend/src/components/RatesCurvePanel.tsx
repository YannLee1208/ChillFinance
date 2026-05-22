import { useQueries } from "@tanstack/react-query";
import ReactECharts from "echarts-for-react";
import { useMemo } from "react";

import { fetchIndicatorSnapshot } from "../api";
import type { IndicatorDefinition } from "../types";

type RatesCurvePanelProps = {
  indicators: IndicatorDefinition[];
};

const TENOR_ORDER: Record<string, number> = {
  "3M": 0.25,
  "2Y": 2,
  "5Y": 5,
  "10Y": 10,
  "30Y": 30,
};

export function RatesCurvePanel({ indicators }: RatesCurvePanelProps) {
  const treasuryIndicators = indicators
    .filter((indicator) => indicator.selectors.country === "United States")
    .filter((indicator) => indicator.selectors.metric === "Yield")
    .sort((left, right) => {
      const leftTenor = TENOR_ORDER[left.selectors.tenor] ?? left.display_order;
      const rightTenor = TENOR_ORDER[right.selectors.tenor] ?? right.display_order;
      return leftTenor - rightTenor;
    });

  const results = useQueries({
    queries: treasuryIndicators.map((indicator) => ({
      queryKey: ["indicator", indicator.code],
      queryFn: () => fetchIndicatorSnapshot(indicator.code),
    })),
  });

  const curvePoints = results
    .map((result) => result.data)
    .filter((snapshot) => snapshot?.latest)
    .map((snapshot) => ({
      tenor: snapshot!.definition.selectors.tenor,
      value: Number(snapshot!.latest!.value),
      period: snapshot!.latest!.period,
    }));

  const latestDate = curvePoints.map((point) => point.period).sort().at(-1);
  const option = useMemo(
    () => ({
      animation: false,
      grid: { bottom: 34, left: 52, right: 18, top: 28 },
      tooltip: {
        trigger: "axis",
        valueFormatter: (value: number) => `${value.toFixed(2)}%`,
      },
      xAxis: {
        type: "category",
        data: curvePoints.map((point) => point.tenor),
        axisTick: { show: false },
        axisLine: { lineStyle: { color: "#ccd8e6" } },
        axisLabel: { color: "#64738a", fontSize: 12 },
      },
      yAxis: {
        type: "value",
        name: "%",
        axisLabel: { color: "#64738a", fontSize: 11 },
        splitLine: { lineStyle: { color: "#e7edf5" } },
      },
      series: [
        {
          type: "bar",
          data: curvePoints.map((point) => point.value),
          barWidth: 28,
          itemStyle: { color: "#1457b8", borderRadius: [4, 4, 0, 0] },
        },
      ],
    }),
    [curvePoints],
  );

  if (treasuryIndicators.length === 0) {
    return null;
  }

  return (
    <section className="curve-panel">
      <div className="curve-title">
        <div>
          <span>美国国债最新期限对比</span>
          <h3>3M / 2Y / 5Y / 10Y / 30Y</h3>
        </div>
        <time>{latestDate ? `最新日期 ${latestDate}` : "等待更新"}</time>
      </div>
      {curvePoints.length > 0 ? (
        <ReactECharts notMerge option={option} style={{ height: "260px", width: "100%" }} />
      ) : (
        <div className="empty-chart tall">还没有可绘制的国债期限数据，请先点击“更新本板块数据”。</div>
      )}
    </section>
  );
}
