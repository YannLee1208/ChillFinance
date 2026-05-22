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
const STYLE_COLORS: Record<string, string[]> = {
  price: ["#1f5eff", "#d92d20", "#7c3aed", "#d97706"],
  trade: ["#0e9384", "#b54708", "#1457b8", "#66758a"],
  pmi: ["#7c3aed", "#0e7490", "#b54708", "#475569"],
  finance_flow: ["#b54708", "#d97706", "#92400e", "#ef6820", "#854d0e"],
  finance_stock: ["#1457b8", "#0e7490", "#5b35d5", "#0369a1", "#475569"],
  finance_rate: ["#d92d20", "#b42318", "#7c2d12", "#9f1239"],
  market: ["#475569", "#1457b8", "#0e9384"],
};

function lineType(panelStyle: string | undefined): "solid" | "dashed" | "dotted" {
  if (panelStyle === "pmi" || panelStyle === "finance_rate") {
    return "dashed";
  }
  if (panelStyle === "market") {
    return "dotted";
  }
  return "solid";
}

function symbolForStyle(panelStyle: string | undefined): string {
  if (panelStyle === "pmi" || panelStyle === "finance_rate") {
    return "diamond";
  }
  if (panelStyle === "market") {
    return "triangle";
  }
  return "circle";
}

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
  const panelStyle = snapshots.find((snapshot) => snapshot.definition.selectors.chart_style)
    ?.definition.selectors.chart_style;
  const palette = panelStyle ? STYLE_COLORS[panelStyle] ?? SERIES_COLORS : SERIES_COLORS;
  const seriesData = snapshots
    .map((snapshot, index) => {
      const localized = localizeIndicator(snapshot.definition);
      const scale = displayScale(snapshot.definition.unit, localized.unit);
      const points = filterPointsByRange(snapshot.points, timeRange)
        .map((point) => toDisplayPoint(point, scale))
        .filter((point): point is NonNullable<typeof point> => Boolean(point));
      return {
        name: localized.name,
        color: palette[index % palette.length],
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
          showSymbol: panelStyle === "pmi",
          symbol: symbolForStyle(panelStyle),
          symbolSize: panelStyle === "pmi" ? 5 : 4,
          smooth: panelStyle === "price",
          step: panelStyle === "finance_stock" ? "end" : false,
          lineStyle: {
            type: lineType(panelStyle),
            width: panelStyle === "trade" || panelStyle === "finance_flow" ? 2 : 2.8,
          },
          areaStyle:
            panelStyle === "price" || panelStyle === "finance_stock"
              ? { opacity: 0.08 }
              : undefined,
          emphasis: { focus: "series" },
        };
      }),
    }),
    [panelStyle, periods, seriesData, unit],
  );

  if (seriesData.length < 2) {
    return null;
  }

  return (
    <article className={`comparison-panel chart-style-${panelStyle ?? "default"}`}>
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
