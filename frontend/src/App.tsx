import { useIsFetching, useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useMemo, useState } from "react";

import { fetchCatalog, fetchLatestIngestionRun, ingestDomain } from "./api";
import { DashboardHeader } from "./components/DashboardHeader";
import { DomainUpdatePanel } from "./components/DomainUpdatePanel";
import { DomainSidebar } from "./components/DomainSidebar";
import { IndicatorGrid } from "./components/IndicatorGrid";
import { OverviewPanel } from "./components/OverviewPanel";
import { RatesCurvePanel } from "./components/RatesCurvePanel";
import { SelectorBar } from "./components/SelectorBar";
import { TimeRangeBar } from "./components/TimeRangeBar";
import type { TimeRangeKey } from "./components/timeRange";

const DEFAULT_DOMAIN = "rates";

export default function App() {
  const [activeDomain, setActiveDomain] = useState(DEFAULT_DOMAIN);
  const [selectedFilters, setSelectedFilters] = useState<Record<string, string>>({});
  const [timeRange, setTimeRange] = useState<TimeRangeKey>("3y");
  const queryClient = useQueryClient();
  const {
    data: catalog = [],
    isError,
    isLoading,
  } = useQuery({
    queryKey: ["catalog"],
    queryFn: fetchCatalog,
  });
  const isRefreshing =
    useIsFetching({ queryKey: ["catalog"] }) + useIsFetching({ queryKey: ["indicator"] }) > 0;

  const selectedIndicators = useMemo(
    () => catalog.filter((indicator) => indicator.domain === activeDomain),
    [activeDomain, catalog],
  );
  const { data: latestRun, isLoading: isRunLoading } = useQuery({
    queryKey: ["ingest-run", activeDomain],
    queryFn: () => fetchLatestIngestionRun(activeDomain),
  });
  const ingestMutation = useMutation({
    mutationFn: () => ingestDomain(activeDomain),
    onSuccess: (run) => {
      queryClient.setQueryData(["ingest-run", activeDomain], run);
      void Promise.all([
        queryClient.invalidateQueries({ queryKey: ["catalog"] }),
        queryClient.invalidateQueries({ queryKey: ["indicator"] }),
      ]);
    },
  });
  const filteredIndicators = useMemo(
    () =>
      selectedIndicators.filter((indicator) =>
        Object.entries(selectedFilters).every(
          ([key, value]) => indicator.selectors[key] === value,
        ),
      ),
    [selectedFilters, selectedIndicators],
  );
  const selectDomain = (domain: string) => {
    setActiveDomain(domain);
    setSelectedFilters({});
  };
  const refreshDashboard = () => {
    void Promise.all([
      queryClient.invalidateQueries({ queryKey: ["catalog"] }),
      queryClient.invalidateQueries({ queryKey: ["indicator"] }),
    ]);
  };

  if (isLoading) {
    return <main className="state-panel">正在加载宏观指标目录</main>;
  }

  if (isError) {
    return <main className="state-panel">无法连接后端服务</main>;
  }

  return (
    <div className="app-shell">
      <DashboardHeader
        activeDomain={activeDomain}
        indicatorCount={filteredIndicators.length}
        isRefreshing={isRefreshing}
        onRefresh={refreshDashboard}
      />
      <div className="dashboard-body">
        <DomainSidebar
          activeDomain={activeDomain}
          catalog={catalog}
          onSelectDomain={selectDomain}
        />
        <main className="content">
          <OverviewPanel activeDomain={activeDomain} indicators={filteredIndicators} />
          <DomainUpdatePanel
            activeDomain={activeDomain}
            isLoading={isRunLoading}
            isUpdating={ingestMutation.isPending}
            latestRun={ingestMutation.data ?? latestRun}
            onUpdate={() => ingestMutation.mutate()}
          />
          <SelectorBar
            indicators={selectedIndicators}
            onChange={setSelectedFilters}
            selected={selectedFilters}
          />
          <TimeRangeBar onChange={setTimeRange} value={timeRange} />
          {activeDomain === "rates" ? (
            <RatesCurvePanel indicators={selectedIndicators} timeRange={timeRange} />
          ) : null}
          <IndicatorGrid indicators={filteredIndicators} timeRange={timeRange} />
        </main>
      </div>
    </div>
  );
}
