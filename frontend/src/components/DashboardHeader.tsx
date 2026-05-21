import { RefreshCw } from "lucide-react";

import { DOMAIN_LABELS } from "./DomainSidebar";

type DashboardHeaderProps = {
  activeDomain: string;
  indicatorCount: number;
  isRefreshing: boolean;
  onRefresh: () => void;
};

export function DashboardHeader({
  activeDomain,
  indicatorCount,
  isRefreshing,
  onRefresh,
}: DashboardHeaderProps) {
  const runDay = new Date().toISOString().slice(0, 10);
  const currentTheme = DOMAIN_LABELS[activeDomain]?.title ?? activeDomain;

  return (
    <header className="dashboard-header">
      <div className="header-title">
        <p className="eyebrow">LOCAL-FIRST GLOBAL MACRO MONITOR</p>
        <h1>全球宏观监测器</h1>
        <p className="header-meta">
          运行日 {runDay}<span aria-hidden="true">/</span>当前主题 {currentTheme}
          <span aria-hidden="true">/</span>指标数 {indicatorCount}
        </p>
      </div>
      <button className="refresh-button" type="button" onClick={onRefresh}>
        <RefreshCw className={isRefreshing ? "spin" : undefined} size={18} />
        刷新
      </button>
    </header>
  );
}
