import type { Observation } from "../types";

export type TimeRangeKey = "6m" | "1y" | "3y" | "5y" | "all";

export const TIME_RANGE_OPTIONS: Array<{ key: TimeRangeKey; label: string }> = [
  { key: "6m", label: "近6个月" },
  { key: "1y", label: "近1年" },
  { key: "3y", label: "近3年" },
  { key: "5y", label: "近5年" },
  { key: "all", label: "全部" },
];

const RANGE_MONTHS: Record<Exclude<TimeRangeKey, "all">, number> = {
  "6m": 6,
  "1y": 12,
  "3y": 36,
  "5y": 60,
};

export function filterPointsByRange(points: Observation[], range: TimeRangeKey): Observation[] {
  if (range === "all" || points.length === 0) {
    return points;
  }

  const latestPeriod = points[points.length - 1].period;
  const cutoff = new Date(`${latestPeriod}T00:00:00`);
  cutoff.setMonth(cutoff.getMonth() - RANGE_MONTHS[range]);
  const cutoffDate = cutoff.toISOString().slice(0, 10);
  return points.filter((point) => point.period >= cutoffDate);
}
