import { useQueries } from "@tanstack/react-query";

import { fetchIndicatorSnapshot } from "../api";
import type { IndicatorDefinition, IndicatorSnapshot } from "../types";
import { ComparisonPanel } from "./ComparisonPanel";
import { IndicatorCard } from "./IndicatorCard";
import { localizeIndicator, localizeSelectorValue } from "./localization";
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

const GROUP_ORDER = [
  "经济总量",
  "CPI",
  "PPI",
  "制造业PMI",
  "非制造业PMI",
  "消费",
  "工业与投资",
  "其他价格指标",
  "进出口",
  "出口",
  "进口",
  "顺逆差",
  "汇率与金融",
  "用电量",
  "发电结构",
  "碳价",
  "市场指数",
  "现货价格",
  "价格",
  "持仓与储备",
  "库存",
  "期货",
  "指数",
  "综合指数",
];

function availabilityText(indicator: IndicatorDefinition, fallbackDescription: string): string {
  const availability = indicator.availability;
  if (!availability || availability.status === "available") {
    return fallbackDescription;
  }
  return [availability.reason, availability.next_step ? `下一步：${availability.next_step}` : ""]
    .filter(Boolean)
    .join(" ");
}

function displayGroup(snapshot: IndicatorSnapshot): string {
  return (
    snapshot.definition.selectors.display_group ||
    snapshot.definition.selectors.category ||
    "其他"
  );
}

function groupSnapshots(snapshots: IndicatorSnapshot[]): [string, IndicatorSnapshot[]][] {
  const grouped = new Map<string, IndicatorSnapshot[]>();
  for (const snapshot of snapshots) {
    const group = displayGroup(snapshot);
    grouped.set(group, [...(grouped.get(group) ?? []), snapshot]);
  }
  return Array.from(grouped.entries()).sort(([left], [right]) => {
    const leftIndex = GROUP_ORDER.indexOf(left);
    const rightIndex = GROUP_ORDER.indexOf(right);
    if (leftIndex === -1 && rightIndex === -1) {
      return left.localeCompare(right, "zh-CN");
    }
    if (leftIndex === -1) {
      return 1;
    }
    if (rightIndex === -1) {
      return -1;
    }
    return leftIndex - rightIndex;
  });
}

function sectionClassName(group: string): string {
  if (["CPI", "PPI", "制造业PMI", "非制造业PMI", "出口", "进口", "顺逆差"].includes(group)) {
    return "indicator-grid grouped-row";
  }
  return "indicator-grid";
}

function comparisonGroups(snapshots: IndicatorSnapshot[]): [string, IndicatorSnapshot[]][] {
  const grouped = new Map<string, IndicatorSnapshot[]>();
  for (const snapshot of snapshots) {
    const group = snapshot.definition.selectors.compare_group;
    if (!group) {
      continue;
    }
    grouped.set(group, [...(grouped.get(group) ?? []), snapshot]);
  }
  return Array.from(grouped.entries()).filter(([, items]) => items.length >= 2);
}

function comparisonAnchorGroup(items: IndicatorSnapshot[]): string {
  const groups = Array.from(new Set(items.map((snapshot) => displayGroup(snapshot))));
  if (groups.includes("CPI") && groups.includes("PPI")) {
    return "CPI";
  }
  const pmiGroups = groups.filter((group) => group.includes("PMI"));
  if (pmiGroups.length > 0) {
    return pmiGroups[0];
  }
  return groups[0] ?? "其他";
}

function comparisonGroupsByAnchor(
  allComparisonGroups: [string, IndicatorSnapshot[]][],
): Map<string, [string, IndicatorSnapshot[]][]> {
  const grouped = new Map<string, [string, IndicatorSnapshot[]][]>();
  for (const [compareGroup, items] of allComparisonGroups) {
    const anchor = comparisonAnchorGroup(items);
    grouped.set(anchor, [...(grouped.get(anchor) ?? []), [compareGroup, items]]);
  }
  return grouped;
}

function localComparisonGroups(
  groupItems: IndicatorSnapshot[],
  allComparisonGroups: [string, IndicatorSnapshot[]][],
): [string, IndicatorSnapshot[]][] {
  const sectionCodes = new Set(groupItems.map((snapshot) => snapshot.definition.code));
  return allComparisonGroups
    .map(
      ([group, items]): [string, IndicatorSnapshot[]] => [
        group,
        items.filter((item) => sectionCodes.has(item.definition.code)),
      ],
    )
    .filter(([, items]) => items.length >= 2);
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
  const allComparisonGroups = comparisonGroups(availableSnapshots);
  const anchoredComparisonGroups = comparisonGroupsByAnchor(allComparisonGroups);

  return (
    <>
      {availableSnapshots.length > 0 ? (
        <>
          {groupSnapshots(availableSnapshots).map(([group, groupItems]) => (
            <section className="indicator-section" key={group}>
              <div className="indicator-section-head">
                <h2>{localizeSelectorValue(group)}</h2>
                <span>{groupItems.length} 个指标</span>
              </div>
              {(anchoredComparisonGroups.get(group) ?? localComparisonGroups(groupItems, allComparisonGroups)).map(([compareGroup, compareItems]) => (
                <ComparisonPanel
                  group={compareGroup}
                  key={compareGroup}
                  snapshots={compareItems}
                  timeRange={timeRange}
                />
              ))}
              <div className={sectionClassName(group)}>
                {groupItems.map((snapshot) => (
                  <IndicatorCard
                    key={snapshot.definition.code}
                    snapshot={snapshot}
                    timeRange={timeRange}
                  />
                ))}
              </div>
            </section>
          ))}
        </>
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
