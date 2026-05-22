import ReactECharts from "echarts-for-react";
import { useMemo } from "react";

import type { IndicatorSnapshot } from "../types";
import { displayScale, formatValue, toDisplayPoint } from "./IndicatorCard";
import { localizeIndicator, localizeSelectorValue } from "./localization";
import { filterPointsByRange, type TimeRangeKey } from "./timeRange";

type ComparisonPanelProps = {
  group: string;
  snapshots: IndicatorSnapshot[];
  timeRange: TimeRangeKey;
};

const SERIES_COLORS = ["#1457b8", "#b42318", "#04706b", "#b54708", "#5b35d5", "#0e7490"];

function commonUnit(snapshots: IndicatorSnapshot[]): string {
  const units = new Set(
    snapshots.map((snapshot) => {
      const localized = localizeIndicator(snapshot.definition);
      return displayScale(snapshot.definition.unit, localized.unit).unit;
    }),
  );
  return units.size === 1 ? Array.from(units)[0] : "";
}

export function ComparisonPanel({ group, snapshots, timeRange }: ComparisonPanelProps) {
  const unit = commonUnit(snapshots);
  const seriesData = snapshots
    .map((snapshot, index) => {
      const localized = localizeIndicator(snapshot.definition);
      const scale = displayScale(snapshot.definition.unit, localized.unit);
      const points = filterPointsByRange(snapshot.points, timeRange)
        .map((point) => toDisplayPoint(point, scale))
        .filter((point): point is NonNullable<typeof point> => Boolean(point));
      return {
        name: localized.name,
        color: SERIES_COLORS[index % SERIES_COLORS.length],
        points,
      };
    })
    .filter((series) => series.points.length > 0);

  const periods = Array.from(
    new Set(seriesData.flatMap((series) => series.points.map((point) => point.period))),
  ).sort();

  const chartOption = useMemo(
    () => ({
      animation: false,
      color: seriesData.map((series) => series.color),
      grid: { bottom: 44, left: 58, right: 22, top: 48 },
      legend: {
        top: 8,
        type: "scroll",
        textStyle: { color: "#334155", fontSize: 11 },
      },
      tooltip: {
        trigger: "axis",
        backgroundColor: "rgba(23, 32, 51, 0.92)",
        borderWidth: 0,
        textStyle: { color: "#fff" },
        valueFormatter: (value: number) => `${formatValue(value)}${unit}`,
      },
      xAxis: {
        type: "category",
        boundaryGap: false,
        data: periods,
        axisLine: { lineStyle: { color: "#cfd8e6" } },
        axisLabel: { color: "#64738a", fontSize: 10, hideOverlap: true },
        axisTick: { show: false },
      },
      yAxis: {
        type: "value",
        scale: true,
        axisLabel: {
          color: "#64738a",
          fontSize: 10,
          formatter: (value: number) => formatValue(value),
        },
        splitLine: { lineStyle: { color: "#e7edf5" } },
      },
      series: seriesData.map((series) => {
        const valuesByPeriod = new Map(
          series.points.map((point) => [point.period, point.displayValue] as const),
        );
        return {
          name: series.name,
          type: "line",
          data: periods.map((period) => valuesByPeriod.get(period) ?? null),
          connectNulls: false,
          showSymbol: false,
          smooth: false,
          lineStyle: { width: 2.5 },
          emphasis: { focus: "series" },
        };
      }),
    }),
    [periods, seriesData, unit],
  );

  if (seriesData.length < 2) {
    return null;
  }

  return (
    <article className="comparison-panel">
      <div className="comparison-head">
        <div>
          <span>综合比较</span>
          <h3>{localizeSelectorValue(group)}</h3>
        </div>
        <strong>
          {seriesData.length} 条序列{unit ? ` / ${unit}` : ""}
        </strong>
      </div>
      <ReactECharts notMerge option={chartOption} style={{ height: "280px", width: "100%" }} />
    </article>
  );
}
