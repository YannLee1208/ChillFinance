# PREGRESS

## 2026-05-21 Task 5

### 进展

- 完成 FastAPI 与 CLI：新增 `backend.app.create_app()`，提供 `/health`、`/api/catalog`、`/api/indicators/{indicator_code}` 和 `/api/observations/{indicator_code}`。
- 新增 `backend.cli` Typer 入口，支持 `init-db` 初始化指标目录，以及 `ingest --provider seed|fred` 采集观测值。
- 新增 `.gitignore`，忽略 `data/`、Python 缓存、pytest/ruff 缓存和后续前端构建产物，避免 CLI smoke 生成的 DuckDB 文件入库。

### 教训

- DuckDB 文件不适合并发跑两个 CLI smoke；`init-db` 和 `ingest` 需要顺序执行，避免同一个 `data/macro.duckdb` 被进程锁住。
- 当前环境里 `rg` 仍然因权限问题无法使用，继续用 PowerShell 原生命令完成文件发现和检查。

### 提交记录

- 待提交：`feat: expose macro api and cli`。

## 2026-05-21

### 进展

- 使用 `superpowers:writing-plans` 为本地个人宏观数据爬取和展示项目编写实施计划。
- 查看了 `example` 目录截图，提炼出左侧主题导航、顶部运行信息、主体指标卡片、曲线图和解读面板的前端布局方向。
- 计划文件保存到 `docs/superpowers/plans/2026-05-21-local-macro-monitor.md`。

### 教训

- 当前目录只有 `example` 截图素材，还不是 git 仓库；执行计划时需要先决定是否 `git init`。
- 本机 `rg --files` 执行被拒绝，本轮改用 PowerShell 原生命令检查文件。
- 宏观数据源跨度较大，第一版应先用统一指标目录、存储、API 和前端打通链路，再逐个替换真实数据源。

### 提交记录

- 暂无；当前目录尚未初始化 git。

### TODO

- 选择执行方式：Subagent-Driven 或 Inline Execution。
- 执行计划中的项目初始化、后端、数据采集、API 和前端任务。
- 后续优先接入中国宏观、全球国债曲线、EIA 能源、LME/SHFE 库存、煤炭和电力真实数据源。

### 进展

- 完成 Task 1 项目初始化：新增项目级 Agent 规则、README、环境变量示例、Python 项目配置、后端配置入口和 pytest 公共 fixture。
- 通过 `backend.constant` 统一默认数据库路径、HTTP 超时、User-Agent、日期格式和 FRED 国债期限序列常量。
- 通过 `backend.config.Settings` 读取本地运行配置，并保留 `.env` 文件加载能力。

### 教训

- `pytest -q` 在当前只有 `tests/conftest.py`、没有实际测试用例时会返回退出码 1，并提示 `no tests ran`；后续任务应增加具体 `test_*.py` 用例后再以 pytest 作为通过门禁。
- `python -m pip install -e ".[dev]"` 会生成 `local_macro_monitor.egg-info` 和 `.pytest_cache`，提交前需要确认这些构建/缓存产物不进入版本控制。

### 提交记录

- 待提交：`feat: bootstrap macro monitor project`。

### TODO

- Task 2 开始前补充首个可执行测试用例，避免 pytest 空跑。

### 进展

- 根据 Task 1 code review 调整 `backend.config.Settings`：忽略 `.env` 中前端专用变量等额外键，并允许使用字段名初始化配置对象。

### 教训

- `pydantic-settings` 读取 dotenv 时会把未声明键纳入校验；如果项目共享 `.env` 给前后端，后端 Settings 需要显式 `extra="ignore"`。
- 使用 PowerShell 写临时 `.env` 时要注意 UTF-8 BOM 对首个键名的影响；验证 dotenv 读取时改用无 BOM 写入更可靠。

### 提交记录

- 待提交：`fix: make backend settings tolerate frontend env`。

### 进展

- 完成 Task 2 领域模型与指标目录：新增 `IndicatorDefinition`、`Observation`、`IndicatorSnapshot` 和 `MacroDataProvider` 协议。
- 通过 `backend.domain.catalog` 汇总 FRED 美国国债收益率指标和宏观/商品/能源种子指标，并支持按代码查询。
- 新增 `tests/test_catalog.py`，覆盖领域集合、美国 10 年期国债收益率字段和指标代码唯一性。

### 教训

- 指标目录先用稳定的 `display_order` 排序，后续前端展示和数据拉取可以共享同一份定义，避免多处维护。

### 提交记录

- 待提交：`feat: add macro indicator catalog`。

### TODO

- 后续数据源任务实现时，让适配器遵循 `backend.domain.providers.MacroDataProvider`。

### 进展

- 完成 Task 3 DuckDB 存储：新增 `DuckDBMacroStore`，支持初始化指标与观测值表、批量 upsert、按指标读取序列和最新观测值。
- 新增 `tests/test_duckdb_store.py`，覆盖观测值写入读取、最新值查询，以及同一指标同一期数据替换。

### 教训

- DuckDB 返回 `decimal(20, 6)` 后会保留六位小数，测试中应显式断言 `Decimal("1.230000")` 这类存储精度。
- 项目 Ruff 规则会要求 Python 3.11 使用 `datetime.UTC` 替代 `timezone.utc`。

### 提交记录

- 待提交：`feat: add duckdb macro storage`。

### 进展

- 根据 Task 3 code review 修复 DuckDB 批量写入：`upsert_indicators` 与 `upsert_observations` 现在使用显式事务，任一行失败会回滚整个批次。
- 增加入库时间转换策略：带时区 `datetime` 先转换为 UTC 再去掉 `tzinfo`，无时区 `datetime` 保持原样。
- 补充观测值批量写入原子性和 +08:00 时间规范化回归测试。

### 教训

- `executemany` 不等于业务批次原子性；涉及多行 upsert 时需要显式事务包住整个批次。
- DuckDB decimal 溢出会抛出 `ConversionException`，测试应断言具体异常类型，避免 Ruff 的裸异常捕获告警。

### 提交记录

- 待提交：`fix: make duckdb batch writes atomic`。

### 进展

- 完成 Task 4 FRED Treasury Parser And Seed Provider：新增 `backend.ingest` 包、FRED CSV 解析、FRED 美国国债收益率适配器、离线种子数据适配器和采集服务。
- 新增 `tests/test_fred_parser.py`，覆盖 FRED 缺失值 `.` 跳过逻辑和 Decimal 值解析。

### 教训

- 本机 `rg` 仍然执行受限，文件发现继续使用 PowerShell 原生命令。
- pandas 读取 FRED CSV 后需要统一处理 `NaN`、空字符串和 `.`，再进入 Decimal 转换，避免缺失值混入观测序列。

### 提交记录

- 待提交：`feat: add macro ingestion providers`。
