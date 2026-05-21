import { useQuery } from "@tanstack/react-query";
import { useMemo, useState } from "react";

import { fetchCatalog } from "./api";
import { DashboardHeader } from "./components/DashboardHeader";
import { DomainSidebar } from "./components/DomainSidebar";
import { IndicatorGrid } from "./components/IndicatorGrid";
import { OverviewPanel } from "./components/OverviewPanel";

const DEFAULT_DOMAIN = "rates";

export default function App() {
  const [activeDomain, setActiveDomain] = useState(DEFAULT_DOMAIN);
  const {
    data: catalog = [],
    isError,
    isLoading,
    refetch,
    isFetching,
  } = useQuery({
    queryKey: ["catalog"],
    queryFn: fetchCatalog,
  });

  const selectedIndicators = useMemo(
    () => catalog.filter((indicator) => indicator.domain === activeDomain),
    [activeDomain, catalog],
  );

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
        indicatorCount={selectedIndicators.length}
        isRefreshing={isFetching}
        onRefresh={() => void refetch()}
      />
      <div className="dashboard-body">
        <DomainSidebar
          activeDomain={activeDomain}
          catalog={catalog}
          onSelectDomain={setActiveDomain}
        />
        <main className="content">
          <OverviewPanel activeDomain={activeDomain} indicators={selectedIndicators} />
          <IndicatorGrid indicators={selectedIndicators} />
        </main>
      </div>
    </div>
  );
}
