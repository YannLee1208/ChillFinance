import ReactECharts from "echarts-for-react";
import { useMemo } from "react";

import type { IndicatorSnapshot } from "../types";

type IndicatorCardProps = {
  snapshot: IndicatorSnapshot;
};

function formatValue(value: string | undefined): string {
  if (value === undefined) {
    return "--";
  }
  const numericValue = Number(value);
  if (!Number.isFinite(numericValue)) {
    return value;
  }
  return new Intl.NumberFormat("zh-CN", {
    maximumFractionDigits: Math.abs(numericValue) >= 1000 ? 0 : 2,
  }).format(numericValue);
}

function formatChange(latestValue: string | undefined, previousValue: string | undefined): number | null {
  if (latestValue === undefined || previousValue === undefined) {
    return null;
  }
  const latest = Number(latestValue);
  const previous = Number(previousValue);
  if (!Number.isFinite(latest) || !Number.isFinite(previous)) {
    return null;
  }
  return latest - previous;
}

export function IndicatorCard({ snapshot }: IndicatorCardProps) {
  const { definition, latest, previous, points } = snapshot;
  const change = formatChange(latest?.value, previous?.value);
  const hasPoints = points.length > 0;

  const chartOption = useMemo(
    () => ({
      animation: false,
      grid: { bottom: 24, left: 44, right: 14, top: 18 },
      tooltip: {
        trigger: "axis",
        valueFormatter: (value: number) => formatValue(String(value)),
      },
      xAxis: {
        type: "category",
        boundaryGap: false,
        data: points.map((point) => point.period),
        axisLine: { lineStyle: { color: "#ccd8e6" } },
        axisLabel: { color: "#64738a", fontSize: 10, hideOverlap: true },
        axisTick: { show: false },
      },
      yAxis: {
        type: "value",
        axisLabel: { color: "#64738a", fontSize: 10 },
        splitLine: { lineStyle: { color: "#e7edf5" } },
      },
      series: [
        {
          type: "line",
          data: points.map((point) => Number(point.value)),
          showSymbol: false,
          smooth: true,
          lineStyle: { color: "#1457b8", width: 2 },
          areaStyle: { color: "rgba(20, 87, 184, 0.1)" },
        },
      ],
    }),
    [points],
  );

  return (
    <article className="indicator-card">
      <div className="card-topline">
        <div>
          <h3>{definition.name}</h3>
          <span>{Object.values(definition.selectors).join(" / ") || definition.region}</span>
        </div>
        <time dateTime={latest?.period}>{latest?.period ?? "暂无日期"}</time>
      </div>

      <div className="metric-row">
        <strong>{formatValue(latest?.value)}</strong>
        <span>{definition.unit}</span>
        {change !== null ? (
          <em className={change >= 0 ? "change up" : "change down"}>
            {change >= 0 ? "+" : ""}
            {formatValue(String(change))}
          </em>
        ) : (
          <em className="change muted">--</em>
        )}
      </div>

      <div className="chart-box">
        {hasPoints ? (
          <ReactECharts
            notMerge
            option={chartOption}
            style={{ height: "190px", width: "100%" }}
          />
        ) : (
          <div className="empty-chart">暂无序列</div>
        )}
      </div>

      <p className="reading">
        {definition.description} 来源 {definition.source}，频率 {definition.frequency}。
      </p>
    </article>
  );
}
