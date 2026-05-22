# PREGRESS

## 2026-05-21

### 进展

- 初始化本地宏观数据监控项目。
- 建立指标目录、DuckDB 存储、FRED/World Bank 采集、FastAPI API 和 React 仪表盘。
- MVP 覆盖国债利率、各国经济、有色、原油、煤炭、电力的领域入口。
- 完成质量门检查：后端 Ruff、pytest 与前端生产构建均已运行。
- 移除默认 seed provider，保留为开发备用。

### 教训

- 先用统一指标目录和种子数据打通链路，可以降低一次性接入多个不稳定数据源的风险。
- 真实数据源应按主题逐个接入 provider，保持接口不变。
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

## 2026-05-22

### 进展

- 新增板块级前端更新按钮，用户点击后会在页面显示成功、失败、写入条数和逐指标原因。
- 新增采集运行记录表 `ingestion_runs` 与 `ingestion_attempts`，支持保存不同数据源的更新尝试。
- 国债利率页新增美国 3M / 2Y / 5Y / 10Y / 30Y 最新收益率对比图。
- 中国宏观新增实际 GDP、社融、人民币贷款、M1、M2、M1-M2 剪刀差等指标入口。
- 真实接入 ChinaData.live 的中国 M2 序列；无法稳定公开抓取的中国指标明确记录为待接入 Wind/官方源，不写模拟数据。
- 修正主要前端中文文案，保证非技术用户可以直接在页面读懂状态。

### 教训

- “能访问数据源但返回 0 条”不能算作成功，应在前端提示为无可写入观测值。
- FRED、World Bank、ChinaData.live 这类公共源适合先做稳定可验证接入；央行/NBS 高频细项仍需要更明确的官方接口或 Wind Key。
- Codex in-app browser 后端当前无法被自动化工具发现，但本地 5173/8000 服务可通过 HTTP 正常访问。

### 提交记录

- 待提交：板块级采集反馈、中国 M2 数据源、国债期限对比图。

### TODO

- 接入 Wind 或官方接口后，替换中国实际 GDP、社融、人民币贷款、M1 与 M1-M2 剪刀差的占位失败记录。
- 继续接入 EIA、LME/SHFE 等需要 Key 或更稳定接口的数据源。
