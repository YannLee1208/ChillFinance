import { useQueries } from "@tanstack/react-query";
import ReactECharts from "echarts-for-react";
import { useMemo } from "react";

import { fetchIndicatorSnapshot } from "../api";
import type { IndicatorDefinition } from "../types";
import { filterPointsByRange, type TimeRangeKey } from "./timeRange";

type RatesCurvePanelProps = {
  indicators: IndicatorDefinition[];
  timeRange: TimeRangeKey;
};

const TENOR_ORDER: Record<string, number> = {
  "3M": 0.25,
  "2Y": 2,
  "5Y": 5,
  "10Y": 10,
  "30Y": 30,
};

export function RatesCurvePanel({ indicators, timeRange }: RatesCurvePanelProps) {
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
    .map((snapshot) => {
      const points = filterPointsByRange(snapshot!.points, timeRange);
      const latest = points.at(-1) ?? snapshot!.latest!;
      return {
        tenor: snapshot!.definition.selectors.tenor,
        value: Number(latest.value),
        period: latest.period,
      };
    });

  const latestDate = curvePoints.map((point) => point.period).sort().at(-1);
  const option = useMemo(
    () => ({
      animation: false,
      grid: { bottom: 36, left: 54, right: 24, top: 34 },
      tooltip: {
        trigger: "axis",
        backgroundColor: "rgba(23, 32, 51, 0.92)",
        borderWidth: 0,
        textStyle: { color: "#fff" },
        valueFormatter: (value: number) => `${value.toFixed(2)}%`,
      },
      xAxis: {
        type: "category",
        data: curvePoints.map((point) => point.tenor),
        axisTick: { show: false },
        axisLine: { lineStyle: { color: "#cfd8e6" } },
        axisLabel: { color: "#64738a", fontSize: 12, fontWeight: 700 },
      },
      yAxis: {
        type: "value",
        scale: true,
        name: "%",
        axisLabel: { color: "#64738a", fontSize: 11 },
        splitLine: { lineStyle: { color: "#e7edf5" } },
      },
      series: [
        {
          type: "line",
          data: curvePoints.map((point) => point.value),
          symbol: "circle",
          symbolSize: 9,
          lineStyle: { color: "#04706b", width: 2.5 },
          itemStyle: { color: "#04706b" },
          label: {
            show: true,
            formatter: (params: { value: number }) => `${Number(params.value).toFixed(2)}%`,
            color: "#334155",
            fontWeight: 800,
          },
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
          <span>美国国债最新期限结构</span>
          <h3>收益率曲线：3M / 2Y / 5Y / 10Y / 30Y</h3>
        </div>
        <time>{latestDate ? `最新日期 ${latestDate}` : "等待更新"}</time>
      </div>
      {curvePoints.length > 0 ? (
        <ReactECharts notMerge option={option} style={{ height: "300px", width: "100%" }} />
      ) : (
        <div className="empty-chart tall">还没有可绘制的国债期限数据，请先点击“更新本板块数据”。</div>
      )}
    </section>
  );
}
