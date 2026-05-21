# PREGRESS

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
