import ReactECharts from "echarts-for-react";
import { useMemo } from "react";

import type { IndicatorSnapshot, Observation } from "../types";
import { latestInRange, localizeIndicator, selectorSummary } from "./localization";
import { filterPointsByRange, type TimeRangeKey } from "./timeRange";

type IndicatorCardProps = {
  snapshot: IndicatorSnapshot;
  timeRange: TimeRangeKey;
};

const LINE_COLORS = ["#1f5eff", "#d92d20", "#039855", "#d97706", "#7c3aed", "#0e9384"];

function colorForCode(code: string): string {
  const total = code.split("").reduce((sum, char) => sum + char.charCodeAt(0), 0);
  return LINE_COLORS[total % LINE_COLORS.length];
}

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

function changeText(change: number | null, unit: string): string {
  if (change === null) {
    return "--";
  }
  if (unit === "%") {
    return `${change >= 0 ? "+" : ""}${Math.round(change * 100)}bp`;
  }
  return `${change >= 0 ? "+" : ""}${formatValue(String(change))}`;
}

function referenceValue(points: Observation[]): number | null {
  if (points.length < 2) {
    return null;
  }
  const previous = Number(points[points.length - 2].value);
  return Number.isFinite(previous) ? previous : null;
}

export function IndicatorCard({ snapshot, timeRange }: IndicatorCardProps) {
  const { definition } = snapshot;
  const localized = localizeIndicator(definition);
  const points = filterPointsByRange(snapshot.points, timeRange);
  const latest = latestInRange(points) ?? snapshot.latest;
  const previous = points.length >= 2 ? points[points.length - 2] : snapshot.previous;
  const change = formatChange(latest?.value, previous?.value);
  const hasPoints = points.length > 0;
  const lineColor = colorForCode(definition.code);
  const refValue = referenceValue(points);

  const chartOption = useMemo(
    () => ({
      animation: false,
      grid: { bottom: 30, left: 46, right: 18, top: 24 },
      tooltip: {
        trigger: "axis",
        backgroundColor: "rgba(23, 32, 51, 0.92)",
        borderWidth: 0,
        textStyle: { color: "#fff" },
        valueFormatter: (value: number) => `${formatValue(String(value))}${localized.unit}`,
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
        axisLabel: { color: "#64738a", fontSize: 10 },
        splitLine: { lineStyle: { color: "#e7edf5" } },
      },
      series: [
        {
          type: "line",
          data: points.map((point) => Number(point.value)),
          showSymbol: false,
          smooth: false,
          lineStyle: { color: lineColor, width: 2.4 },
          areaStyle: { color: `${lineColor}14` },
          markLine:
            refValue === null
              ? undefined
              : {
                  symbol: "none",
                  label: {
                    formatter: "上一期 {c}",
                    color: "#334155",
                    fontWeight: 700,
                  },
                  lineStyle: { color: "#718198", type: "dashed", width: 2 },
                  data: [{ yAxis: refValue }],
                },
          markPoint:
            latest === null
              ? undefined
              : {
                  symbol: "circle",
                  symbolSize: 8,
                  itemStyle: { color: lineColor },
                  label: {
                    formatter: `最新 ${latest.period} · ${formatValue(latest.value)}`,
                    color: "#334155",
                    fontWeight: 800,
                    position: "left",
                  },
                  data: [{ coord: [latest.period, Number(latest.value)] }],
                },
        },
      ],
    }),
    [latest, lineColor, localized.unit, points, refValue],
  );

  return (
    <article className="indicator-card">
      <div className="card-topline">
        <div>
          <h3>{localized.name}</h3>
          <span>{selectorSummary(definition)}</span>
        </div>
        <time dateTime={latest?.period}>{latest?.period ?? "暂无日期"}</time>
      </div>

      <div className="metric-row">
        <strong>{formatValue(latest?.value)}</strong>
        <span>{localized.unit}</span>
        <em className={change === null ? "change muted" : change >= 0 ? "change up" : "change down"}>
          {changeText(change, localized.unit)}
        </em>
      </div>

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
        <b>读图</b> {localized.description} 来源：{localized.sourceLabel}；当前窗口 {points.length} 个观测点。
      </p>
    </article>
  );
}
