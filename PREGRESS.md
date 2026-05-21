# PREGRESS

## 2026-05-21

### 进展

- 初始化本地宏观数据监控项目。
- 建立指标目录、DuckDB 存储、FRED/World Bank 采集、FastAPI API 和 React 仪表盘。
- MVP 已覆盖国债利率、各国经济、有色、原油、煤炭、电力的领域入口。
- 完成 Task 7 质量门检查：后端 Ruff、pytest 与前端生产构建均已运行。

### 教训

- 先用统一指标目录和种子数据打通链路，可以降低一次性接入多个不稳定数据源的风险。
- 真实数据源应按主题逐个接入 provider，保持接口不变。
- seed provider 已从默认指标目录移除，仅保留为开发备用。
- DuckDB 批量写入需要显式事务，时间戳应先归一到 UTC 再落库。
- 前端刷新要同时刷新目录和指标快照，避免展示陈旧图表。
- 当前环境中 `rg` 可被发现但执行被拒，必要时用 PowerShell 原生命令完成文件发现与检查。
- Vite 生产构建会提示 ECharts 相关 chunk 较大，后续可按页面或图表组件拆分加载。

### 提交记录

- `04dafd9 docs: add macro monitor implementation plan`
- `287be01 feat: bootstrap macro monitor project`
- `02a16e2 fix: make backend settings tolerate frontend env`
- `62ba31a feat: add macro indicator catalog`
- `64afb4c test: cover treasury catalog metadata`
- `7243859 feat: add duckdb macro storage`
- `574458b fix: make duckdb batch writes atomic`
- `59e6ed9 feat: add macro ingestion providers`
- `ac332d7 feat: expose macro api and cli`
- `c73e1eb fix: validate api indicators and cli providers`
- `aec3fff feat: add macro dashboard frontend`
- `ebaaed7 fix: refresh dashboard indicator data`

### TODO

- 接入中国宏观官方数据或 Wind。
- 接入 EIA / FRED 能源数据。
- 接入 LME/SHFE 库存和产能指标。
- 增加调度任务和数据质量告警。
