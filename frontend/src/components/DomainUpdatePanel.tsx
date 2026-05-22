import { RefreshCw } from "lucide-react";

import type { IngestionRunRecord } from "../types";
import { DOMAIN_LABELS } from "./DomainSidebar";

type DomainUpdatePanelProps = {
  activeDomain: string;
  latestRun: IngestionRunRecord | null | undefined;
  isLoading: boolean;
  isUpdating: boolean;
  onUpdate: () => void;
};

function formatDateTime(value: string | undefined): string {
  if (!value) {
    return "还没有更新记录";
  }
  return new Intl.DateTimeFormat("zh-CN", {
    dateStyle: "medium",
    timeStyle: "medium",
  }).format(new Date(value));
}

function statusText(status: IngestionRunRecord["status"] | undefined): string {
  if (status === "success") {
    return "全部成功";
  }
  if (status === "partial") {
    return "部分成功";
  }
  if (status === "failed") {
    return "全部失败";
  }
  return "未更新";
}

export function DomainUpdatePanel({
  activeDomain,
  latestRun,
  isLoading,
  isUpdating,
  onUpdate,
}: DomainUpdatePanelProps) {
  const label = DOMAIN_LABELS[activeDomain]?.title ?? activeDomain;
  const attempts = latestRun?.attempts ?? [];

  return (
    <section className="domain-update-panel">
      <div className="update-head">
        <div>
          <span>数据更新</span>
          <h3>{label}</h3>
        </div>
        <button className="refresh-button" disabled={isUpdating} onClick={onUpdate} type="button">
          <RefreshCw size={17} className={isUpdating ? "spin" : undefined} />
          {isUpdating ? "正在更新" : "更新本板块数据"}
        </button>
      </div>

      <div className="update-summary">
        <strong>{isUpdating ? "正在尝试所有可用数据源" : statusText(latestRun?.status)}</strong>
        <p>
          {isUpdating
            ? "请稍等，页面会在完成后刷新图表，并列出每个指标的真实结果。"
            : latestRun?.message ??
              (isLoading ? "正在读取最近一次更新记录。" : "还没有点击过本板块更新。")}
        </p>
        <time>{formatDateTime(latestRun?.finished_at)}</time>
      </div>

      {attempts.length > 0 ? (
        <div className="attempt-list">
          {attempts.map((attempt) => (
            <article key={`${attempt.run_id}-${attempt.indicator_code}`} className="attempt-row">
              <b className={attempt.status === "success" ? "ok" : "bad"}>
                {attempt.status === "success" ? "成功" : "失败"}
              </b>
              <div>
                <strong>{attempt.indicator_code}</strong>
                <p>{attempt.message}</p>
              </div>
              <span>{attempt.provider}</span>
            </article>
          ))}
        </div>
      ) : null}
    </section>
  );
}
