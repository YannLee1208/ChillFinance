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
- 美国国债收益率切换为美国财政部 Daily Treasury Rates 官方 CSV。
- 中国宏观新增实际 GDP、社融、人民币贷款、M1、M2、M1-M2 剪刀差等指标入口。
- 中国经济扩展为经济总量、消费、工业与投资、房地产、进出口价格、汇率与金融六个专题。
- 追加中国实际 GDP 增速、居民消费支出、资本形成、工业增加值、进出口额、CPI 通胀和官方汇率等真实年度序列。
- 真实接入 ChinaData.live 的中国 M2 序列；无法稳定公开抓取的中国指标明确记录为待接入 Wind/官方源，不写模拟数据。
- 修正主要前端中文文案，保证非技术用户可以直接在页面读懂状态。

### 教训

- “能访问数据源但返回 0 条”不能算作成功，应在前端提示为无可写入观测值。
- FRED、World Bank、ChinaData.live 这类公共源适合先做稳定可验证接入；央行/NBS 高频细项仍需要更明确的官方接口或 Wind Key。
- 美国财政部 CSV 按月份提供；先抓当前月可以稳定绘制最新期限曲线，并避免页面等待过久。
- EIA 官方 API 已验证需要 `api_key`，国家统计局 easyquery 当前环境返回 403。
- Codex in-app browser 后端当前无法被自动化工具发现，但本地 5173/8000 服务可通过 HTTP 正常访问。

### 提交记录

- 待提交：板块级采集反馈、中国 M2 数据源、国债期限对比图。

### TODO

- 接入 Wind 或官方接口后，替换中国实际 GDP、社融、制造业投资、基建投资、地产投资、商品房销售面积与进出口价格指数的占位失败记录。
- 继续接入 EIA、LME/SHFE 等需要 Key 或更稳定接口的数据源。

## 2026-05-22 中国宏观补充接入

### 进展

- 新增 `akshare_china` provider，用 AkShare 抓取东方财富、行情源等公开中国宏观与市场序列。
- 已真实接入并落库：中国季度名义 GDP、中国季度实际 GDP 同比、社零同比、规模以上工业增加值同比、固定资产投资同比、新增信贷、M2、M1、M1-M2 剪刀差、新房价格样本指数、PPI、美元计出口同比、美元计进口同比、上证综指。
- 重写前端指标中文标签，修复此前本地文件里的乱码，并补充新增中国指标的中文名称、单位、来源说明。
- 已触发“中国经济”整板块更新：成功 30 个指标，失败 13 个指标，写入 13172 条观测值。

### 教训

- AkShare 部分接口虽然可用，但必须检查最新日期；`macro_china_rmb` 只到 2021 年，因此未纳入前端目录，避免把陈旧日频数据伪装成最新数据。
- 社融、制造业投资、基建投资、房地产开发投资、商品房销售面积、进出口价格指数仍未找到当前环境可稳定返回的公开接口，继续以前端待接入原因展示，不写模拟数据。

### TODO

- 如后续配置 Wind Key 或拿到稳定官方接口，再替换上述待接入指标。
- 继续寻找中国财政赤字、政府债务口径的稳定公开源；当前 World Bank 对部分债务/财政指标可访问但无可写入观测值。
