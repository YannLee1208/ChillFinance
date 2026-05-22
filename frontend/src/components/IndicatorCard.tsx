import ReactECharts from "echarts-for-react";
import { useMemo } from "react";

import type { IndicatorSnapshot, Observation } from "../types";
import {
  latestInRange,
  localizeIndicator,
  localizeSelectorValue,
  selectorSummary,
} from "./localization";
import { filterPointsByRange, type TimeRangeKey } from "./timeRange";

type IndicatorCardProps = {
  snapshot: IndicatorSnapshot;
  timeRange: TimeRangeKey;
};

const LINE_COLORS = ["#1f5eff", "#d92d20", "#039855", "#d97706", "#7c3aed", "#0e9384"];

type DisplayPoint = Observation & {
  numericValue: number;
  displayValue: number;
};

type DisplayScale = {
  unit: string;
  divisor: number;
};

function colorForCode(code: string): string {
  const total = code.split("").reduce((sum, char) => sum + char.charCodeAt(0), 0);
  return LINE_COLORS[total % LINE_COLORS.length];
}

function displayScale(definitionUnit: string, localizedUnit: string): DisplayScale {
  const normalizedUnit = localizedUnit || definitionUnit;
  if (normalizedUnit === "美元") {
    return { unit: "亿美元", divisor: 100_000_000 };
  }
  if (normalizedUnit === "百万美元") {
    return { unit: "十亿美元", divisor: 1_000 };
  }
  if (definitionUnit === "100 million CNY") {
    return { unit: "亿元", divisor: 1 };
  }
  return { unit: normalizedUnit, divisor: 1 };
}

function toDisplayPoint(point: Observation, scale: DisplayScale): DisplayPoint | null {
  const numericValue = Number(point.value);
  if (!Number.isFinite(numericValue)) {
    return null;
  }
  return {
    ...point,
    numericValue,
    displayValue: numericValue / scale.divisor,
  };
}

function formatValue(value: number | string | undefined): string {
  if (value === undefined) {
    return "--";
  }
  const numericValue = Number(value);
  if (!Number.isFinite(numericValue)) {
    return String(value);
  }
  return new Intl.NumberFormat("zh-CN", {
    maximumFractionDigits: Math.abs(numericValue) >= 1000 ? 0 : 2,
  }).format(numericValue);
}

function formatChange(latestValue: number | undefined, previousValue: number | undefined): number | null {
  if (latestValue === undefined || previousValue === undefined) {
    return null;
  }
  if (!Number.isFinite(latestValue) || !Number.isFinite(previousValue)) {
    return null;
  }
  return latestValue - previousValue;
}

function changeText(change: number | null, unit: string): string {
  if (change === null) {
    return "--";
  }
  if (unit === "%") {
    return `${change >= 0 ? "+" : ""}${Math.round(change * 100)}bp`;
  }
  return `${change >= 0 ? "+" : ""}${formatValue(String(change))}`;
}

function referenceValue(points: DisplayPoint[]): number | null {
  if (points.length < 2) {
    return null;
  }
  return points[points.length - 2].displayValue;
}

function shouldUseBars(frequency: string, pointCount: number): boolean {
  return frequency !== "daily" || pointCount <= 80;
}

function buildSeries(
  points: DisplayPoint[],
  lineColor: string,
  latest: DisplayPoint | null,
  refValue: number | null,
  useBars: boolean,
) {
  const barSeries = useBars
    ? [
        {
          type: "bar",
          data: points.map((point) => point.displayValue),
          barWidth: "58%",
          itemStyle: {
            color: `${lineColor}18`,
            borderRadius: [3, 3, 0, 0],
          },
          tooltip: { show: false },
          silent: true,
        },
      ]
    : [];
  return [
    ...barSeries,
    {
      type: "line",
      data: points.map((point) => point.displayValue),
      showSymbol: false,
      smooth: false,
      emphasis: { focus: "series" },
      lineStyle: { color: lineColor, width: 3 },
      areaStyle: useBars ? undefined : { color: `${lineColor}14` },
      markLine:
        refValue === null
          ? undefined
          : {
              symbol: "none",
              label: { show: false },
              lineStyle: { color: "#718198", type: "dashed", width: 2 },
              data: [{ yAxis: refValue }],
            },
      markPoint:
        latest === null
          ? undefined
          : {
              symbol: "circle",
              symbolSize: 8,
              itemStyle: { color: lineColor, borderColor: "#ffffff", borderWidth: 2 },
              label: { show: false },
              data: [{ coord: [latest.period, latest.displayValue] }],
            },
    },
    ...(useBars
      ? [
          {
            type: "scatter",
            data: points.map((point) => [point.period, point.displayValue]),
            symbolSize: 4,
            itemStyle: { color: lineColor, opacity: 0.72 },
            tooltip: { show: false },
          },
        ]
      : []),
  ];
}

export function IndicatorCard({ snapshot, timeRange }: IndicatorCardProps) {
  const { definition } = snapshot;
  const localized = localizeIndicator(definition);
  const regionLabel = localizeSelectorValue(definition.region);
  const scale = displayScale(definition.unit, localized.unit);
  const rawPoints = filterPointsByRange(snapshot.points, timeRange);
  const points = rawPoints
    .map((point) => toDisplayPoint(point, scale))
    .filter((point): point is DisplayPoint => Boolean(point));
  const latestRaw = latestInRange(rawPoints) ?? snapshot.latest;
  const previousRaw = rawPoints.length >= 2 ? rawPoints.at(-2) : snapshot.previous;
  const latest = latestRaw ? toDisplayPoint(latestRaw, scale) : null;
  const previous = previousRaw ? toDisplayPoint(previousRaw, scale) : null;
  const change = formatChange(latest?.displayValue, previous?.displayValue);
  const hasPoints = points.length > 0;
  const lineColor = colorForCode(definition.code);
  const refValue = referenceValue(points);
  const useBars = shouldUseBars(definition.frequency, points.length);

  const chartOption = useMemo(
    () => ({
      animation: false,
      grid: { bottom: 34, left: 54, right: 18, top: 34 },
      tooltip: {
        trigger: "axis",
        backgroundColor: "rgba(23, 32, 51, 0.92)",
        borderWidth: 0,
        textStyle: { color: "#fff" },
        valueFormatter: (value: number) => `${formatValue(value)}${scale.unit}`,
      },
      xAxis: {
        type: "category",
        boundaryGap: false,
        data: points.map((point) => point.period),
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
      series: buildSeries(points, lineColor, latest, refValue, useBars),
    }),
    [latest, lineColor, points, refValue, scale.unit, useBars],
  );

  return (
    <article className="indicator-card">
      <div className="card-topline">
        <div>
          <h3>{localized.name}</h3>
          {definition.domain === "country_macro" ? <small>{regionLabel}</small> : null}
          <span>{selectorSummary(definition)}</span>
        </div>
        <time dateTime={latest?.period}>{latest?.period ?? "暂无日期"}</time>
      </div>

      <div className="metric-row">
        <strong>{formatValue(latest?.displayValue)}</strong>
        <span>{scale.unit}</span>
        <em className={change === null ? "change muted" : change >= 0 ? "change up" : "change down"}>
          {changeText(change, scale.unit)}
        </em>
      </div>

      {hasPoints ? (
        <div className="focus-strip">
          <span>最新 {latest?.period ?? "--"}</span>
          <b>上期 {formatValue(previous?.displayValue)}</b>
          <b>{changeText(change, scale.unit)}</b>
        </div>
      ) : null}

      <div className="chart-box professional">
        {hasPoints ? (
          <ReactECharts
            notMerge
            option={chartOption}
            style={{ height: "220px", width: "100%" }}
          />
        ) : (
          <div className="empty-chart">暂无可展示序列；请查看上方更新记录中的数据源反馈。</div>
        )}
      </div>

      <p className="reading">
        <b>读图</b> {localized.description} 来源：{localized.sourceLabel}；当前窗口 {points.length} 个观测点，{useBars ? "柱形表示读数强弱，折线和散点强调变化节奏。" : "折线强调高频趋势，虚线为上一期参考。"}
      </p>
    </article>
  );
}
