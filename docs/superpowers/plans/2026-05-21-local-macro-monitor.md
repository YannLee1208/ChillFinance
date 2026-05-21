# Local Macro Monitor Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a local personal macro data collection and dashboard project covering sovereign rates, country macro data, non-ferrous metals, crude oil, coal, power, and future extensions.

**Architecture:** Use a local-first Python backend with typed indicator definitions, pluggable data providers, DuckDB persistence, FastAPI read APIs, and scheduled ingestion jobs. Use a React dashboard that follows the example screenshots: left domain navigation, top run metadata, dense chart cards, metric summaries, and drill-down pages.

**Tech Stack:** Python 3.11+, FastAPI, DuckDB, Pandas, Pydantic, APScheduler, httpx, pytest, Vite, React, TypeScript, TanStack Query, ECharts, lucide-react.

---

## Scope

This plan builds a working MVP, not every final indicator. The MVP must include:

- A stable indicator catalog covering all requested domains.
- Real ingestion for U.S. Treasury rates from FRED CSV.
- Seed/mock adapters for country macro, non-ferrous, crude oil, coal, and power so the UI and storage contracts are testable before every paid or rate-limited data source is wired.
- A provider interface that can later add Wind, official statistical APIs, EIA, Eurostat, World Bank, exchange warehouse data, and internal `otter` capabilities.
- A dashboard that can display current values, historical series, source freshness, and extension status.

Deferred to later plans:

- Production-grade anti-blocking crawlers for every website.
- User authentication.
- Cloud deployment.
- Alert notification through enterprise WeChat.

## Referenced Example UI

The `example/*.jpg` screenshots show a wide, dense macro dashboard:

- Header with project title, author/run day/data window, and a refresh action.
- Left sidebar grouping domains such as sovereign rates, regional economies, A-share monitoring, indicators, and policy functions.
- Main content using repeated metric cards with latest value, change, expected/next value, line chart, and short reading text.
- Secondary cards for curve/term-structure analysis and bullet summaries.

The frontend tasks below preserve that information density while using a local app structure.

## Environment Variables

Maintain these in `env.example` and `README.md`:

- `MACRO_DB_PATH`: local DuckDB file path, default `data/macro.duckdb`.
- `FRED_API_KEY`: optional FRED key for future JSON API use. MVP Treasury CSV ingestion works without it.
- `MACRO_HTTP_TIMEOUT_SECONDS`: HTTP timeout for external sources, default `30`.
- `MACRO_USER_AGENT`: crawler user agent string for public data downloads.
- `VITE_API_BASE_URL`: frontend API base URL, default `http://127.0.0.1:8000`.

## File Structure

Create this structure:

```text
E:\code\finance
├── AGENTS.md
├── PREGRESS.md
├── README.md
├── env.example
├── pyproject.toml
├── backend
│   ├── __init__.py
│   ├── app.py
│   ├── cli.py
│   ├── config.py
│   ├── constant.py
│   ├── domain
│   │   ├── __init__.py
│   │   ├── catalog.py
│   │   ├── models.py
│   │   └── providers.py
│   ├── ingest
│   │   ├── __init__.py
│   │   ├── fred.py
│   │   ├── seed.py
│   │   └── service.py
│   └── storage
│       ├── __init__.py
│       └── duckdb_store.py
├── frontend
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── src
│       ├── App.tsx
│       ├── api.ts
│       ├── main.tsx
│       ├── types.ts
│       ├── styles.css
│       └── components
│           ├── DashboardHeader.tsx
│           ├── DomainSidebar.tsx
│           ├── IndicatorCard.tsx
│           ├── IndicatorGrid.tsx
│           └── OverviewPanel.tsx
└── tests
    ├── conftest.py
    ├── test_catalog.py
    ├── test_duckdb_store.py
    ├── test_fred_parser.py
    └── test_api.py
```

Responsibilities:

- `backend/constant.py`: shared constants only.
- `backend/config.py`: environment parsing and path defaults.
- `backend/domain/models.py`: typed domain objects.
- `backend/domain/catalog.py`: indicator definitions and display grouping.
- `backend/domain/providers.py`: provider protocols for future data adapters.
- `backend/ingest/fred.py`: U.S. Treasury CSV fetch/parse.
- `backend/ingest/seed.py`: deterministic seed data for domains without live adapters.
- `backend/ingest/service.py`: orchestrates ingestion by indicator.
- `backend/storage/duckdb_store.py`: schema creation and series upsert/query.
- `backend/app.py`: FastAPI API surface.
- `backend/cli.py`: local commands for initializing DB, ingesting data, and serving API.
- `frontend/src/*`: local dashboard UI.

## Task 1: Project Bootstrap And Local Rules

**Files:**
- Create: `E:\code\finance\AGENTS.md`
- Create: `E:\code\finance\README.md`
- Create: `E:\code\finance\env.example`
- Create: `E:\code\finance\pyproject.toml`
- Create: `E:\code\finance\backend\__init__.py`
- Create: `E:\code\finance\backend\constant.py`
- Create: `E:\code\finance\backend\config.py`
- Create: `E:\code\finance\tests\conftest.py`

- [ ] **Step 1: Create project-specific agent instructions**

Write `AGENTS.md`:

```markdown
# Finance Project Agent Instructions

本项目是本地优先的个人宏观数据监控系统。

- Python 代码遵循 PEP 8，使用类型注解；公开 API 写 docstring。
- 注释使用中文，解释业务原因，不重复代码字面意思。
- 公用常量放在 `backend/constant.py`。
- 本地路径、API Key、数据库路径通过环境变量或配置传入，不写死绝对路径。
- 新增环境变量时同步更新 `env.example` 和 `README.md`。
- 数据源适配器要实现 `backend.domain.providers.MacroDataProvider`。
- 有测试时先写 pytest，再实现。
- 进展、教训、提交记录、后续事项写入 `PREGRESS.md`。
```

- [ ] **Step 2: Create README**

Write `README.md`:

```markdown
# Local Macro Monitor

本项目用于在本地采集、存储和展示个人宏观数据，覆盖国债利率、主要经济体宏观指标、有色、原油、煤炭、电力以及后续扩展主题。

## 第一阶段范围

- 国债利率：接入 FRED 的美国国债期限利率 CSV。
- 国家宏观：中国、美国、日本、欧洲的 GDP、财政赤字、债务规模先建立指标定义和种子数据。
- 大宗与能源：金银铜铝、原油、成品油、油运、煤炭、电力先建立指标定义和种子数据。
- 前端：本地仪表盘，左侧主题导航，右侧图表卡片和概览分析。

## 环境变量

| 变量名 | 用途 | 默认值 |
| --- | --- | --- |
| `MACRO_DB_PATH` | 本地 DuckDB 数据库路径 | `data/macro.duckdb` |
| `FRED_API_KEY` | FRED API Key，后续 JSON API 可用 | 空 |
| `MACRO_HTTP_TIMEOUT_SECONDS` | HTTP 请求超时时间 | `30` |
| `MACRO_USER_AGENT` | 公共数据下载 User-Agent | `local-macro-monitor/0.1` |
| `VITE_API_BASE_URL` | 前端访问的后端地址 | `http://127.0.0.1:8000` |

## 本地开发

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
python -m backend.cli init-db
python -m backend.cli ingest --provider seed
python -m backend.cli ingest --provider fred
uvicorn backend.app:create_app --factory --reload
```

前端开发：

```powershell
cd frontend
npm install
npm run dev
```

## 测试

```powershell
pytest -q
```
```

- [ ] **Step 3: Create env example**

Write `env.example`:

```dotenv
MACRO_DB_PATH=data/macro.duckdb
FRED_API_KEY=
MACRO_HTTP_TIMEOUT_SECONDS=30
MACRO_USER_AGENT=local-macro-monitor/0.1
VITE_API_BASE_URL=http://127.0.0.1:8000
```

- [ ] **Step 4: Create Python packaging config**

Write `pyproject.toml`:

```toml
[build-system]
requires = ["setuptools>=69", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "local-macro-monitor"
version = "0.1.0"
description = "Local-first macro data ingestion and dashboard."
requires-python = ">=3.11"
dependencies = [
    "apscheduler>=3.10,<4",
    "duckdb>=1.0,<2",
    "fastapi>=0.111,<1",
    "httpx>=0.27,<1",
    "pandas>=2.2,<3",
    "pydantic>=2.7,<3",
    "pydantic-settings>=2.3,<3",
    "typer>=0.12,<1",
    "uvicorn[standard]>=0.30,<1",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.2,<9",
    "pytest-asyncio>=0.23,<1",
    "ruff>=0.5,<1",
]

[tool.setuptools.packages.find]
include = ["backend*"]

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B"]

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
```

- [ ] **Step 5: Create constants**

Write `backend/constant.py`:

```python
"""项目级常量。"""

from pathlib import Path

DEFAULT_DB_PATH = Path("data/macro.duckdb")
DEFAULT_HTTP_TIMEOUT_SECONDS = 30
DEFAULT_USER_AGENT = "local-macro-monitor/0.1"

DATE_FORMAT = "%Y-%m-%d"

FRED_TREASURY_SERIES = {
    "US_DGS3MO": "DGS3MO",
    "US_DGS2": "DGS2",
    "US_DGS5": "DGS5",
    "US_DGS10": "DGS10",
    "US_DGS30": "DGS30",
}
```

- [ ] **Step 6: Create config**

Write `backend/config.py`:

```python
"""应用配置读取。"""

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from backend.constant import (
    DEFAULT_DB_PATH,
    DEFAULT_HTTP_TIMEOUT_SECONDS,
    DEFAULT_USER_AGENT,
)


class Settings(BaseSettings):
    """本地宏观监控配置。"""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    macro_db_path: Path = Field(default=DEFAULT_DB_PATH, alias="MACRO_DB_PATH")
    fred_api_key: str | None = Field(default=None, alias="FRED_API_KEY")
    macro_http_timeout_seconds: int = Field(
        default=DEFAULT_HTTP_TIMEOUT_SECONDS,
        alias="MACRO_HTTP_TIMEOUT_SECONDS",
    )
    macro_user_agent: str = Field(default=DEFAULT_USER_AGENT, alias="MACRO_USER_AGENT")


def get_settings() -> Settings:
    """返回当前运行配置。"""

    return Settings()
```

- [ ] **Step 7: Create pytest path setup**

Write `tests/conftest.py`:

```python
"""测试公共配置。"""

from collections.abc import Iterator
from pathlib import Path

import pytest


@pytest.fixture()
def temp_db_path(tmp_path: Path) -> Iterator[Path]:
    """提供临时 DuckDB 路径。"""

    yield tmp_path / "macro.duckdb"
```

- [ ] **Step 8: Run bootstrap checks**

Run:

```powershell
python -m pip install -e ".[dev]"
pytest -q
```

Expected:

```text
no tests ran
```

- [ ] **Step 9: Commit if git is initialized**

Run:

```powershell
git status --short
```

If this is a git repository, run:

```powershell
git add AGENTS.md README.md env.example pyproject.toml backend tests
git commit -m "feat: bootstrap macro monitor project"
```

If git is not initialized, record this in `PREGRESS.md`.

## Task 2: Domain Models And Indicator Catalog

**Files:**
- Create: `E:\code\finance\backend\domain\__init__.py`
- Create: `E:\code\finance\backend\domain\models.py`
- Create: `E:\code\finance\backend\domain\catalog.py`
- Create: `E:\code\finance\backend\domain\providers.py`
- Test: `E:\code\finance\tests\test_catalog.py`

- [ ] **Step 1: Write failing catalog tests**

Write `tests/test_catalog.py`:

```python
"""指标目录测试。"""

from backend.domain.catalog import get_catalog, get_indicator


def test_catalog_contains_requested_domains() -> None:
    catalog = get_catalog()
    domains = {indicator.domain for indicator in catalog}

    assert {
        "rates",
        "country_macro",
        "nonferrous",
        "crude_oil",
        "coal",
        "power",
    }.issubset(domains)


def test_us_treasury_indicator_has_frequency_and_unit() -> None:
    indicator = get_indicator("US_DGS10")

    assert indicator.name == "U.S. Treasury 10Y yield"
    assert indicator.frequency == "daily"
    assert indicator.unit == "%"
    assert indicator.provider == "fred"


def test_catalog_codes_are_unique() -> None:
    catalog = get_catalog()
    codes = [indicator.code for indicator in catalog]

    assert len(codes) == len(set(codes))
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```powershell
pytest tests/test_catalog.py -q
```

Expected:

```text
ModuleNotFoundError: No module named 'backend.domain'
```

- [ ] **Step 3: Create domain models**

Write `backend/domain/models.py`:

```python
"""宏观指标领域模型。"""

from datetime import date, datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field

Frequency = Literal["daily", "weekly", "monthly", "quarterly", "annual"]


class IndicatorDefinition(BaseModel):
    """指标定义。"""

    code: str
    name: str
    domain: str
    region: str
    unit: str
    frequency: Frequency
    provider: str
    source: str
    description: str
    display_order: int = 0


class Observation(BaseModel):
    """单个指标观测值。"""

    indicator_code: str
    period: date
    value: Decimal
    provider: str
    source: str
    ingested_at: datetime


class IndicatorSnapshot(BaseModel):
    """前端展示用指标快照。"""

    definition: IndicatorDefinition
    latest: Observation | None
    previous: Observation | None
    points: list[Observation] = Field(default_factory=list)
```

- [ ] **Step 4: Create provider protocol**

Write `backend/domain/providers.py`:

```python
"""数据源适配器接口。"""

from typing import Protocol

from backend.domain.models import IndicatorDefinition, Observation


class MacroDataProvider(Protocol):
    """宏观数据源适配器协议。"""

    name: str

    def supports(self, indicator: IndicatorDefinition) -> bool:
        """判断当前适配器是否支持该指标。"""

    async def fetch(self, indicator: IndicatorDefinition) -> list[Observation]:
        """拉取指标观测值。"""
```

- [ ] **Step 5: Create indicator catalog**

Write `backend/domain/catalog.py`:

```python
"""宏观指标目录。"""

from backend.constant import FRED_TREASURY_SERIES
from backend.domain.models import IndicatorDefinition


def _treasury_indicators() -> list[IndicatorDefinition]:
    tenors = {
        "US_DGS3MO": "U.S. Treasury 3M yield",
        "US_DGS2": "U.S. Treasury 2Y yield",
        "US_DGS5": "U.S. Treasury 5Y yield",
        "US_DGS10": "U.S. Treasury 10Y yield",
        "US_DGS30": "U.S. Treasury 30Y yield",
    }
    return [
        IndicatorDefinition(
            code=code,
            name=name,
            domain="rates",
            region="United States",
            unit="%",
            frequency="daily",
            provider="fred",
            source=f"FRED:{fred_code}",
            description="美国财政部固定期限国债收益率。",
            display_order=index,
        )
        for index, (code, fred_code) in enumerate(FRED_TREASURY_SERIES.items(), start=1)
        for name in [tenors[code]]
    ]


_SEED_INDICATORS = [
    IndicatorDefinition(
        code="CN_GDP_YOY",
        name="China GDP YoY",
        domain="country_macro",
        region="China",
        unit="%",
        frequency="quarterly",
        provider="seed",
        source="seed:country_macro",
        description="中国实际 GDP 同比增速，后续接入国家统计局或 Wind。",
        display_order=101,
    ),
    IndicatorDefinition(
        code="US_FISCAL_DEFICIT",
        name="U.S. fiscal deficit",
        domain="country_macro",
        region="United States",
        unit="USD bn",
        frequency="monthly",
        provider="seed",
        source="seed:country_macro",
        description="美国财政赤字，后续接入 Treasury 或 FRED。",
        display_order=102,
    ),
    IndicatorDefinition(
        code="EU_DEBT_TO_GDP",
        name="Euro Area debt to GDP",
        domain="country_macro",
        region="Euro Area",
        unit="%",
        frequency="quarterly",
        provider="seed",
        source="seed:country_macro",
        description="欧元区政府债务占 GDP 比重，后续接入 Eurostat。",
        display_order=103,
    ),
    IndicatorDefinition(
        code="JP_GDP_YOY",
        name="Japan GDP YoY",
        domain="country_macro",
        region="Japan",
        unit="%",
        frequency="quarterly",
        provider="seed",
        source="seed:country_macro",
        description="日本实际 GDP 同比增速，后续接入官方统计。",
        display_order=104,
    ),
    IndicatorDefinition(
        code="CU_LME_INVENTORY",
        name="LME copper inventory",
        domain="nonferrous",
        region="Global",
        unit="tonne",
        frequency="daily",
        provider="seed",
        source="seed:nonferrous",
        description="LME 铜库存，后续接入交易所或 Wind。",
        display_order=201,
    ),
    IndicatorDefinition(
        code="OIL_BRENT_PRICE",
        name="Brent crude oil price",
        domain="crude_oil",
        region="Global",
        unit="USD/bbl",
        frequency="daily",
        provider="seed",
        source="seed:crude_oil",
        description="Brent 原油价格，后续接入 EIA 或交易所数据。",
        display_order=301,
    ),
    IndicatorDefinition(
        code="COAL_QHD_PRICE",
        name="Qinhuangdao thermal coal price",
        domain="coal",
        region="China",
        unit="CNY/tonne",
        frequency="weekly",
        provider="seed",
        source="seed:coal",
        description="秦皇岛动力煤价格，后续接入行业数据源。",
        display_order=401,
    ),
    IndicatorDefinition(
        code="CN_POWER_GENERATION",
        name="China power generation",
        domain="power",
        region="China",
        unit="TWh",
        frequency="monthly",
        provider="seed",
        source="seed:power",
        description="中国发电量，后续接入国家统计局或 Wind。",
        display_order=501,
    ),
]


def get_catalog() -> list[IndicatorDefinition]:
    """返回全部指标定义。"""

    return sorted([*_treasury_indicators(), *_SEED_INDICATORS], key=lambda item: item.display_order)


def get_indicator(code: str) -> IndicatorDefinition:
    """按代码查找指标定义。"""

    for indicator in get_catalog():
        if indicator.code == code:
            return indicator
    raise KeyError(f"Unknown indicator code: {code}")
```

- [ ] **Step 6: Run catalog tests**

Run:

```powershell
pytest tests/test_catalog.py -q
```

Expected:

```text
3 passed
```

- [ ] **Step 7: Commit if git is initialized**

```powershell
git add backend/domain tests/test_catalog.py
git commit -m "feat: add macro indicator catalog"
```

## Task 3: DuckDB Storage

**Files:**
- Create: `E:\code\finance\backend\storage\__init__.py`
- Create: `E:\code\finance\backend\storage\duckdb_store.py`
- Test: `E:\code\finance\tests\test_duckdb_store.py`

- [ ] **Step 1: Write failing storage tests**

Write `tests/test_duckdb_store.py`:

```python
"""DuckDB 存储测试。"""

from datetime import date, datetime, timezone
from decimal import Decimal

from backend.domain.models import IndicatorDefinition, Observation
from backend.storage.duckdb_store import DuckDBMacroStore


def test_store_upserts_and_reads_observations(temp_db_path) -> None:
    store = DuckDBMacroStore(temp_db_path)
    store.initialize()
    definition = IndicatorDefinition(
        code="TEST_SERIES",
        name="Test series",
        domain="rates",
        region="Test",
        unit="%",
        frequency="daily",
        provider="test",
        source="test",
        description="测试指标。",
    )
    observations = [
        Observation(
            indicator_code="TEST_SERIES",
            period=date(2026, 1, 1),
            value=Decimal("1.23"),
            provider="test",
            source="test",
            ingested_at=datetime(2026, 1, 2, tzinfo=timezone.utc),
        ),
        Observation(
            indicator_code="TEST_SERIES",
            period=date(2026, 1, 2),
            value=Decimal("1.25"),
            provider="test",
            source="test",
            ingested_at=datetime(2026, 1, 3, tzinfo=timezone.utc),
        ),
    ]

    store.upsert_indicators([definition])
    store.upsert_observations(observations)

    loaded = store.get_series("TEST_SERIES")
    latest = store.get_latest("TEST_SERIES")

    assert [item.value for item in loaded] == [Decimal("1.230000"), Decimal("1.250000")]
    assert latest is not None
    assert latest.period == date(2026, 1, 2)


def test_store_replaces_same_indicator_period(temp_db_path) -> None:
    store = DuckDBMacroStore(temp_db_path)
    store.initialize()
    first = Observation(
        indicator_code="TEST_SERIES",
        period=date(2026, 1, 1),
        value=Decimal("1.23"),
        provider="test",
        source="test",
        ingested_at=datetime(2026, 1, 2, tzinfo=timezone.utc),
    )
    second = first.model_copy(update={"value": Decimal("1.99")})

    store.upsert_observations([first])
    store.upsert_observations([second])

    loaded = store.get_series("TEST_SERIES")

    assert len(loaded) == 1
    assert loaded[0].value == Decimal("1.990000")
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```powershell
pytest tests/test_duckdb_store.py -q
```

Expected:

```text
ModuleNotFoundError: No module named 'backend.storage'
```

- [ ] **Step 3: Implement DuckDB store**

Write `backend/storage/duckdb_store.py`:

```python
"""DuckDB 本地存储。"""

from collections.abc import Iterable
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path

import duckdb

from backend.domain.models import IndicatorDefinition, Observation


class DuckDBMacroStore:
    """本地宏观数据 DuckDB 存储。"""

    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path

    def initialize(self) -> None:
        """初始化数据库表。"""

        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with duckdb.connect(str(self.db_path)) as conn:
            conn.execute(
                """
                create table if not exists indicators (
                    code varchar primary key,
                    name varchar not null,
                    domain varchar not null,
                    region varchar not null,
                    unit varchar not null,
                    frequency varchar not null,
                    provider varchar not null,
                    source varchar not null,
                    description varchar not null,
                    display_order integer not null
                )
                """
            )
            conn.execute(
                """
                create table if not exists observations (
                    indicator_code varchar not null,
                    period date not null,
                    value decimal(20, 6) not null,
                    provider varchar not null,
                    source varchar not null,
                    ingested_at timestamp not null,
                    primary key (indicator_code, period)
                )
                """
            )

    def upsert_indicators(self, indicators: Iterable[IndicatorDefinition]) -> None:
        """写入或更新指标定义。"""

        rows = [
            (
                item.code,
                item.name,
                item.domain,
                item.region,
                item.unit,
                item.frequency,
                item.provider,
                item.source,
                item.description,
                item.display_order,
            )
            for item in indicators
        ]
        if not rows:
            return

        with duckdb.connect(str(self.db_path)) as conn:
            conn.executemany(
                """
                insert or replace into indicators
                values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                rows,
            )

    def upsert_observations(self, observations: Iterable[Observation]) -> None:
        """写入或更新观测值。"""

        rows = [
            (
                item.indicator_code,
                item.period,
                item.value,
                item.provider,
                item.source,
                item.ingested_at.replace(tzinfo=None),
            )
            for item in observations
        ]
        if not rows:
            return

        with duckdb.connect(str(self.db_path)) as conn:
            conn.executemany(
                """
                insert or replace into observations
                values (?, ?, ?, ?, ?, ?)
                """,
                rows,
            )

    def get_series(self, indicator_code: str, limit: int | None = None) -> list[Observation]:
        """读取指标时间序列。"""

        query = """
            select indicator_code, period, value, provider, source, ingested_at
            from observations
            where indicator_code = ?
            order by period
        """
        params: list[str | int] = [indicator_code]
        if limit is not None:
            query += " limit ?"
            params.append(limit)

        with duckdb.connect(str(self.db_path)) as conn:
            rows = conn.execute(query, params).fetchall()
        return [self._row_to_observation(row) for row in rows]

    def get_latest(self, indicator_code: str) -> Observation | None:
        """读取指标最新观测。"""

        with duckdb.connect(str(self.db_path)) as conn:
            row = conn.execute(
                """
                select indicator_code, period, value, provider, source, ingested_at
                from observations
                where indicator_code = ?
                order by period desc
                limit 1
                """,
                [indicator_code],
            ).fetchone()
        if row is None:
            return None
        return self._row_to_observation(row)

    @staticmethod
    def _row_to_observation(row: tuple[str, date, Decimal, str, str, datetime]) -> Observation:
        """将数据库行转换为领域对象。"""

        return Observation(
            indicator_code=row[0],
            period=row[1],
            value=row[2],
            provider=row[3],
            source=row[4],
            ingested_at=row[5],
        )
```

- [ ] **Step 4: Run storage tests**

Run:

```powershell
pytest tests/test_duckdb_store.py -q
```

Expected:

```text
2 passed
```

- [ ] **Step 5: Commit if git is initialized**

```powershell
git add backend/storage tests/test_duckdb_store.py
git commit -m "feat: add duckdb macro storage"
```

## Task 4: FRED Treasury Parser And Seed Provider

**Files:**
- Create: `E:\code\finance\backend\ingest\__init__.py`
- Create: `E:\code\finance\backend\ingest\fred.py`
- Create: `E:\code\finance\backend\ingest\seed.py`
- Create: `E:\code\finance\backend\ingest\service.py`
- Test: `E:\code\finance\tests\test_fred_parser.py`

- [ ] **Step 1: Write failing FRED parser tests**

Write `tests/test_fred_parser.py`:

```python
"""FRED 解析测试。"""

from decimal import Decimal

from backend.ingest.fred import parse_fred_csv


def test_parse_fred_csv_skips_missing_values() -> None:
    csv_text = "DATE,DGS10\n2026-01-01,4.10\n2026-01-02,.\n2026-01-03,4.12\n"

    observations = parse_fred_csv(
        csv_text=csv_text,
        indicator_code="US_DGS10",
        provider="fred",
        source="FRED:DGS10",
    )

    assert len(observations) == 2
    assert observations[0].value == Decimal("4.10")
    assert observations[1].value == Decimal("4.12")
```

- [ ] **Step 2: Run parser test to verify it fails**

Run:

```powershell
pytest tests/test_fred_parser.py -q
```

Expected:

```text
ModuleNotFoundError: No module named 'backend.ingest'
```

- [ ] **Step 3: Implement FRED parser and provider**

Write `backend/ingest/fred.py`:

```python
"""FRED 数据源适配。"""

from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from io import StringIO

import httpx
import pandas as pd

from backend.constant import FRED_TREASURY_SERIES
from backend.domain.models import IndicatorDefinition, Observation


def parse_fred_csv(
    csv_text: str,
    indicator_code: str,
    provider: str,
    source: str,
) -> list[Observation]:
    """解析 FRED CSV 文本为观测值。"""

    frame = pd.read_csv(StringIO(csv_text))
    if len(frame.columns) < 2:
        raise ValueError("FRED CSV must contain DATE and value columns")

    date_column = frame.columns[0]
    value_column = frame.columns[1]
    ingested_at = datetime.now(timezone.utc)
    observations: list[Observation] = []

    for row in frame.itertuples(index=False):
        period_text = getattr(row, date_column)
        value_text = getattr(row, value_column)
        if pd.isna(value_text) or str(value_text).strip() in {"", "."}:
            continue
        try:
            value = Decimal(str(value_text))
        except InvalidOperation as exc:
            raise ValueError(f"Invalid FRED value: {value_text}") from exc
        observations.append(
            Observation(
                indicator_code=indicator_code,
                period=pd.to_datetime(period_text).date(),
                value=value,
                provider=provider,
                source=source,
                ingested_at=ingested_at,
            )
        )

    return observations


class FredTreasuryProvider:
    """FRED 美国国债收益率适配器。"""

    name = "fred"

    def __init__(self, timeout_seconds: int, user_agent: str) -> None:
        self.timeout_seconds = timeout_seconds
        self.user_agent = user_agent

    def supports(self, indicator: IndicatorDefinition) -> bool:
        """判断是否支持该 FRED 国债指标。"""

        return indicator.code in FRED_TREASURY_SERIES

    async def fetch(self, indicator: IndicatorDefinition) -> list[Observation]:
        """下载并解析 FRED CSV。"""

        fred_code = FRED_TREASURY_SERIES[indicator.code]
        url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={fred_code}"
        async with httpx.AsyncClient(
            timeout=self.timeout_seconds,
            headers={"User-Agent": self.user_agent},
        ) as client:
            response = await client.get(url)
            response.raise_for_status()
        return parse_fred_csv(
            csv_text=response.text,
            indicator_code=indicator.code,
            provider=self.name,
            source=indicator.source,
        )
```

- [ ] **Step 4: Implement seed provider**

Write `backend/ingest/seed.py`:

```python
"""确定性种子数据，用于尚未接入真实源的主题。"""

from datetime import date, datetime, timezone
from decimal import Decimal

from backend.domain.models import IndicatorDefinition, Observation

_SEED_VALUES: dict[str, list[tuple[date, Decimal]]] = {
    "CN_GDP_YOY": [(date(2025, 9, 30), Decimal("4.8")), (date(2025, 12, 31), Decimal("5.0"))],
    "US_FISCAL_DEFICIT": [(date(2026, 1, 31), Decimal("-129")), (date(2026, 2, 28), Decimal("-236"))],
    "EU_DEBT_TO_GDP": [(date(2025, 9, 30), Decimal("88.2")), (date(2025, 12, 31), Decimal("87.9"))],
    "JP_GDP_YOY": [(date(2025, 9, 30), Decimal("1.4")), (date(2025, 12, 31), Decimal("1.1"))],
    "CU_LME_INVENTORY": [(date(2026, 5, 1), Decimal("171000")), (date(2026, 5, 2), Decimal("169500"))],
    "OIL_BRENT_PRICE": [(date(2026, 5, 1), Decimal("72.4")), (date(2026, 5, 2), Decimal("73.1"))],
    "COAL_QHD_PRICE": [(date(2026, 4, 24), Decimal("712")), (date(2026, 5, 1), Decimal("719"))],
    "CN_POWER_GENERATION": [(date(2026, 2, 28), Decimal("820")), (date(2026, 3, 31), Decimal("846"))],
}


class SeedProvider:
    """尚未接入真实源时使用的本地种子数据适配器。"""

    name = "seed"

    def supports(self, indicator: IndicatorDefinition) -> bool:
        """判断是否有该指标种子数据。"""

        return indicator.code in _SEED_VALUES

    async def fetch(self, indicator: IndicatorDefinition) -> list[Observation]:
        """返回指标种子观测值。"""

        ingested_at = datetime.now(timezone.utc)
        return [
            Observation(
                indicator_code=indicator.code,
                period=period,
                value=value,
                provider=self.name,
                source=indicator.source,
                ingested_at=ingested_at,
            )
            for period, value in _SEED_VALUES[indicator.code]
        ]
```

- [ ] **Step 5: Implement ingestion service**

Write `backend/ingest/service.py`:

```python
"""指标采集编排服务。"""

from collections.abc import Iterable

from backend.domain.models import IndicatorDefinition
from backend.domain.providers import MacroDataProvider
from backend.storage.duckdb_store import DuckDBMacroStore


class IngestionService:
    """按指标目录执行采集并写入存储。"""

    def __init__(self, store: DuckDBMacroStore, providers: Iterable[MacroDataProvider]) -> None:
        self.store = store
        self.providers = list(providers)

    async def ingest(self, indicators: Iterable[IndicatorDefinition], provider_name: str | None = None) -> int:
        """采集指标并返回写入观测值数量。"""

        total = 0
        indicator_list = list(indicators)
        self.store.upsert_indicators(indicator_list)

        for indicator in indicator_list:
            provider = self._select_provider(indicator, provider_name)
            if provider is None:
                continue
            observations = await provider.fetch(indicator)
            self.store.upsert_observations(observations)
            total += len(observations)

        return total

    def _select_provider(
        self,
        indicator: IndicatorDefinition,
        provider_name: str | None,
    ) -> MacroDataProvider | None:
        for provider in self.providers:
            if provider_name is not None and provider.name != provider_name:
                continue
            if provider.supports(indicator):
                return provider
        return None
```

- [ ] **Step 6: Run FRED parser test**

Run:

```powershell
pytest tests/test_fred_parser.py -q
```

Expected:

```text
1 passed
```

- [ ] **Step 7: Commit if git is initialized**

```powershell
git add backend/ingest tests/test_fred_parser.py
git commit -m "feat: add macro ingestion providers"
```

## Task 5: FastAPI And CLI

**Files:**
- Create: `E:\code\finance\backend\app.py`
- Create: `E:\code\finance\backend\cli.py`
- Test: `E:\code\finance\tests\test_api.py`

- [ ] **Step 1: Write failing API tests**

Write `tests/test_api.py`:

```python
"""API 测试。"""

from fastapi.testclient import TestClient

from backend.app import create_app


def test_health_endpoint() -> None:
    client = TestClient(create_app())

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_catalog_endpoint_contains_rates() -> None:
    client = TestClient(create_app())

    response = client.get("/api/catalog")

    assert response.status_code == 200
    payload = response.json()
    assert any(item["domain"] == "rates" for item in payload)
```

- [ ] **Step 2: Run API tests to verify failure**

Run:

```powershell
pytest tests/test_api.py -q
```

Expected:

```text
ModuleNotFoundError: No module named 'backend.app'
```

- [ ] **Step 3: Implement FastAPI app**

Write `backend/app.py`:

```python
"""FastAPI 应用入口。"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.config import get_settings
from backend.domain.catalog import get_catalog, get_indicator
from backend.domain.models import IndicatorDefinition, IndicatorSnapshot, Observation
from backend.storage.duckdb_store import DuckDBMacroStore


def create_app() -> FastAPI:
    """创建 FastAPI 应用。"""

    app = FastAPI(title="Local Macro Monitor")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/api/catalog", response_model=list[IndicatorDefinition])
    def catalog() -> list[IndicatorDefinition]:
        return get_catalog()

    @app.get("/api/indicators/{indicator_code}", response_model=IndicatorSnapshot)
    def indicator_snapshot(indicator_code: str) -> IndicatorSnapshot:
        try:
            definition = get_indicator(indicator_code)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

        settings = get_settings()
        store = DuckDBMacroStore(settings.macro_db_path)
        store.initialize()
        points = store.get_series(indicator_code)
        latest = points[-1] if points else None
        previous = points[-2] if len(points) >= 2 else None
        return IndicatorSnapshot(
            definition=definition,
            latest=latest,
            previous=previous,
            points=points,
        )

    @app.get("/api/observations/{indicator_code}", response_model=list[Observation])
    def observations(indicator_code: str) -> list[Observation]:
        settings = get_settings()
        store = DuckDBMacroStore(settings.macro_db_path)
        store.initialize()
        return store.get_series(indicator_code)

    return app
```

- [ ] **Step 4: Implement CLI**

Write `backend/cli.py`:

```python
"""本地命令行入口。"""

import asyncio
from typing import Annotated

import typer

from backend.config import get_settings
from backend.domain.catalog import get_catalog
from backend.ingest.fred import FredTreasuryProvider
from backend.ingest.seed import SeedProvider
from backend.ingest.service import IngestionService
from backend.storage.duckdb_store import DuckDBMacroStore

app = typer.Typer(help="Local macro monitor commands.")


@app.command("init-db")
def init_db() -> None:
    """初始化本地数据库。"""

    settings = get_settings()
    store = DuckDBMacroStore(settings.macro_db_path)
    store.initialize()
    store.upsert_indicators(get_catalog())
    typer.echo(f"Initialized database: {settings.macro_db_path}")


@app.command("ingest")
def ingest(
    provider: Annotated[str | None, typer.Option(help="Provider name: seed or fred.")] = None,
) -> None:
    """采集指标数据。"""

    settings = get_settings()
    store = DuckDBMacroStore(settings.macro_db_path)
    store.initialize()
    service = IngestionService(
        store=store,
        providers=[
            SeedProvider(),
            FredTreasuryProvider(
                timeout_seconds=settings.macro_http_timeout_seconds,
                user_agent=settings.macro_user_agent,
            ),
        ],
    )
    total = asyncio.run(service.ingest(get_catalog(), provider_name=provider))
    typer.echo(f"Ingested observations: {total}")


if __name__ == "__main__":
    app()
```

- [ ] **Step 5: Run API tests**

Run:

```powershell
pytest tests/test_api.py -q
```

Expected:

```text
2 passed
```

- [ ] **Step 6: Run CLI smoke tests**

Run:

```powershell
python -m backend.cli init-db
python -m backend.cli ingest --provider seed
```

Expected:

```text
Initialized database: data\macro.duckdb
Ingested observations: 16
```

- [ ] **Step 7: Commit if git is initialized**

```powershell
git add backend/app.py backend/cli.py tests/test_api.py
git commit -m "feat: expose macro api and cli"
```

## Task 6: Frontend Dashboard

**Files:**
- Create: `E:\code\finance\frontend\package.json`
- Create: `E:\code\finance\frontend\index.html`
- Create: `E:\code\finance\frontend\tsconfig.json`
- Create: `E:\code\finance\frontend\vite.config.ts`
- Create: `E:\code\finance\frontend\src\main.tsx`
- Create: `E:\code\finance\frontend\src\App.tsx`
- Create: `E:\code\finance\frontend\src\api.ts`
- Create: `E:\code\finance\frontend\src\types.ts`
- Create: `E:\code\finance\frontend\src\styles.css`
- Create: `E:\code\finance\frontend\src\components\DashboardHeader.tsx`
- Create: `E:\code\finance\frontend\src\components\DomainSidebar.tsx`
- Create: `E:\code\finance\frontend\src\components\IndicatorCard.tsx`
- Create: `E:\code\finance\frontend\src\components\IndicatorGrid.tsx`
- Create: `E:\code\finance\frontend\src\components\OverviewPanel.tsx`

- [ ] **Step 1: Create frontend package**

Write `frontend/package.json`:

```json
{
  "name": "local-macro-monitor-frontend",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "@tanstack/react-query": "^5.51.15",
    "echarts": "^5.5.1",
    "echarts-for-react": "^3.0.2",
    "lucide-react": "^0.468.0",
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
  "devDependencies": {
    "@types/react": "^18.3.3",
    "@types/react-dom": "^18.3.0",
    "@vitejs/plugin-react": "^4.3.1",
    "typescript": "^5.5.4",
    "vite": "^5.3.5"
  }
}
```

- [ ] **Step 2: Create Vite config and HTML**

Write `frontend/index.html`:

```html
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Local Macro Monitor</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

Write `frontend/tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["DOM", "DOM.Iterable", "ES2020"],
    "allowJs": false,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "module": "ESNext",
    "moduleResolution": "Node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx"
  },
  "include": ["src"],
  "references": []
}
```

Write `frontend/vite.config.ts`:

```typescript
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    host: "127.0.0.1",
    port: 5173
  }
});
```

- [ ] **Step 3: Create frontend types and API**

Write `frontend/src/types.ts`:

```typescript
export type IndicatorDefinition = {
  code: string;
  name: string;
  domain: string;
  region: string;
  unit: string;
  frequency: "daily" | "weekly" | "monthly" | "quarterly" | "annual";
  provider: string;
  source: string;
  description: string;
  display_order: number;
};

export type Observation = {
  indicator_code: string;
  period: string;
  value: string;
  provider: string;
  source: string;
  ingested_at: string;
};

export type IndicatorSnapshot = {
  definition: IndicatorDefinition;
  latest: Observation | null;
  previous: Observation | null;
  points: Observation[];
};
```

Write `frontend/src/api.ts`:

```typescript
import type { IndicatorDefinition, IndicatorSnapshot } from "./types";

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";

async function requestJson<T>(path: string): Promise<T> {
  const response = await fetch(`${apiBaseUrl}${path}`);
  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export function fetchCatalog(): Promise<IndicatorDefinition[]> {
  return requestJson<IndicatorDefinition[]>("/api/catalog");
}

export function fetchSnapshot(code: string): Promise<IndicatorSnapshot> {
  return requestJson<IndicatorSnapshot>(`/api/indicators/${code}`);
}
```

- [ ] **Step 4: Create React entry**

Write `frontend/src/main.tsx`:

```typescript
import React from "react";
import ReactDOM from "react-dom/client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import App from "./App";
import "./styles.css";

const queryClient = new QueryClient();

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  </React.StrictMode>
);
```

- [ ] **Step 5: Create dashboard components**

Write `frontend/src/components/DashboardHeader.tsx`:

```typescript
import { RefreshCw } from "lucide-react";

type DashboardHeaderProps = {
  activeDomain: string;
  indicatorCount: number;
};

export function DashboardHeader({ activeDomain, indicatorCount }: DashboardHeaderProps) {
  const runDay = new Date().toISOString().slice(0, 10);

  return (
    <header className="dashboard-header">
      <div>
        <p className="eyebrow">LOCAL-FIRST GLOBAL MACRO MONITOR</p>
        <h1>全球宏观监测器</h1>
        <p className="meta">
          运行日 {runDay} | 当前主题 {activeDomain} | 指标数 {indicatorCount}
        </p>
      </div>
      <button className="refresh-button" type="button" aria-label="刷新页面" onClick={() => window.location.reload()}>
        <RefreshCw size={18} />
        一键刷新
      </button>
    </header>
  );
}
```

Write `frontend/src/components/DomainSidebar.tsx`:

```typescript
import type { IndicatorDefinition } from "../types";

const domainLabels: Record<string, { title: string; subtitle: string }> = {
  rates: { title: "国债利率", subtitle: "期限 / 曲线" },
  country_macro: { title: "各国经济", subtitle: "GDP / 财政 / 债务" },
  nonferrous: { title: "有色板块", subtitle: "金银铜铝 / 库存" },
  crude_oil: { title: "原油板块", subtitle: "原油 / 成品油 / 油运" },
  coal: { title: "煤炭板块", subtitle: "价格 / 库存 / 产能" },
  power: { title: "电力板块", subtitle: "发电 / 用电 / 电煤" }
};

type DomainSidebarProps = {
  catalog: IndicatorDefinition[];
  activeDomain: string;
  onSelectDomain: (domain: string) => void;
};

export function DomainSidebar({ catalog, activeDomain, onSelectDomain }: DomainSidebarProps) {
  const domains = Array.from(new Set(catalog.map((item) => item.domain)));

  return (
    <aside className="sidebar">
      {domains.map((domain) => {
        const label = domainLabels[domain] ?? { title: domain, subtitle: "扩展指标" };
        const isActive = domain === activeDomain;
        return (
          <button
            key={domain}
            className={isActive ? "nav-item active" : "nav-item"}
            type="button"
            onClick={() => onSelectDomain(domain)}
          >
            <span>{label.title}</span>
            <small>{label.subtitle}</small>
          </button>
        );
      })}
    </aside>
  );
}
```

Write `frontend/src/components/IndicatorCard.tsx`:

```typescript
import { useMemo } from "react";
import ReactECharts from "echarts-for-react";
import type { IndicatorSnapshot } from "../types";

type IndicatorCardProps = {
  snapshot: IndicatorSnapshot;
};

export function IndicatorCard({ snapshot }: IndicatorCardProps) {
  const latest = snapshot.latest;
  const previous = snapshot.previous;
  const latestValue = latest ? Number(latest.value) : null;
  const previousValue = previous ? Number(previous.value) : null;
  const change = latestValue !== null && previousValue !== null ? latestValue - previousValue : null;

  const option = useMemo(
    () => ({
      animation: false,
      grid: { left: 40, right: 16, top: 20, bottom: 28 },
      xAxis: {
        type: "category",
        data: snapshot.points.map((point) => point.period),
        axisLabel: { color: "#61708a" }
      },
      yAxis: { type: "value", axisLabel: { color: "#61708a" }, splitLine: { lineStyle: { color: "#e6edf5" } } },
      series: [
        {
          type: "line",
          data: snapshot.points.map((point) => Number(point.value)),
          showSymbol: false,
          lineStyle: { width: 2, color: "#1769e0" },
          areaStyle: { color: "rgba(23, 105, 224, 0.08)" }
        }
      ],
      tooltip: { trigger: "axis" }
    }),
    [snapshot.points]
  );

  return (
    <article className="indicator-card">
      <div className="card-topline">
        <span>{snapshot.definition.name}</span>
        <small>{latest?.period ?? "等待数据"}</small>
      </div>
      <div className="metric-row">
        <strong>{latestValue === null ? "--" : latestValue.toFixed(2)}</strong>
        <span>{snapshot.definition.unit}</span>
        {change !== null && <em className={change >= 0 ? "up" : "down"}>{change >= 0 ? "+" : ""}{change.toFixed(2)}</em>}
      </div>
      <div className="chart-box">
        <ReactECharts option={option} style={{ height: 220 }} />
      </div>
      <p className="reading">
        {snapshot.definition.description} 最新值来自 {snapshot.definition.source}，
        频率为 {snapshot.definition.frequency}。
      </p>
    </article>
  );
}
```

Write `frontend/src/components/IndicatorGrid.tsx`:

```typescript
import { useQueries } from "@tanstack/react-query";
import { fetchSnapshot } from "../api";
import type { IndicatorDefinition } from "../types";
import { IndicatorCard } from "./IndicatorCard";

type IndicatorGridProps = {
  indicators: IndicatorDefinition[];
};

export function IndicatorGrid({ indicators }: IndicatorGridProps) {
  const results = useQueries({
    queries: indicators.map((indicator) => ({
      queryKey: ["snapshot", indicator.code],
      queryFn: () => fetchSnapshot(indicator.code)
    }))
  });

  if (results.some((result) => result.isLoading)) {
    return <div className="state-panel">正在加载指标数据...</div>;
  }

  if (results.some((result) => result.isError)) {
    return <div className="state-panel">指标数据加载失败，请确认后端已启动。</div>;
  }

  return (
    <section className="indicator-grid">
      {results.map((result) => result.data && <IndicatorCard key={result.data.definition.code} snapshot={result.data} />)}
    </section>
  );
}
```

Write `frontend/src/components/OverviewPanel.tsx`:

```typescript
import type { IndicatorDefinition } from "../types";

type OverviewPanelProps = {
  indicators: IndicatorDefinition[];
};

export function OverviewPanel({ indicators }: OverviewPanelProps) {
  const providers = Array.from(new Set(indicators.map((indicator) => indicator.provider))).join(" / ");

  return (
    <section className="overview-panel">
      <h2>主题概览</h2>
      <p>
        当前主题包含 {indicators.length} 个指标，数据源为 {providers}。
        种子数据代表接口已经预留，后续替换为真实适配器即可进入同一展示链路。
      </p>
      <ul>
        <li>优先保证指标定义、存储、API 和图表展示一致。</li>
        <li>真实爬虫按主题逐步接入，避免一次性维护过多不稳定数据源。</li>
        <li>每个指标保留来源、频率、单位和更新时间，便于检查数据质量。</li>
      </ul>
    </section>
  );
}
```

- [ ] **Step 6: Create App layout**

Write `frontend/src/App.tsx`:

```typescript
import { useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { fetchCatalog } from "./api";
import { DashboardHeader } from "./components/DashboardHeader";
import { DomainSidebar } from "./components/DomainSidebar";
import { IndicatorGrid } from "./components/IndicatorGrid";
import { OverviewPanel } from "./components/OverviewPanel";

export default function App() {
  const { data: catalog = [], isLoading, isError } = useQuery({
    queryKey: ["catalog"],
    queryFn: fetchCatalog
  });
  const [activeDomain, setActiveDomain] = useState("rates");

  const indicators = useMemo(
    () => catalog.filter((indicator) => indicator.domain === activeDomain),
    [catalog, activeDomain]
  );

  if (isLoading) {
    return <main className="state-panel">正在加载宏观指标目录...</main>;
  }

  if (isError) {
    return <main className="state-panel">无法连接后端，请先启动 FastAPI。</main>;
  }

  return (
    <div className="app-shell">
      <DashboardHeader activeDomain={activeDomain} indicatorCount={indicators.length} />
      <div className="dashboard-body">
        <DomainSidebar catalog={catalog} activeDomain={activeDomain} onSelectDomain={setActiveDomain} />
        <main className="content">
          <OverviewPanel indicators={indicators} />
          <IndicatorGrid indicators={indicators} />
        </main>
      </div>
    </div>
  );
}
```

- [ ] **Step 7: Create CSS**

Write `frontend/src/styles.css`:

```css
:root {
  color: #172033;
  background: #edf3f8;
  font-family: Inter, "Microsoft YaHei", "PingFang SC", system-ui, sans-serif;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
}

button {
  font: inherit;
}

.app-shell {
  min-height: 100vh;
}

.dashboard-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  padding: 28px 36px;
  background: #ffffff;
  border-bottom: 1px solid #cfdae8;
}

.eyebrow {
  margin: 0 0 8px;
  color: #2465d7;
  font-size: 13px;
  font-weight: 800;
  letter-spacing: 0;
}

h1 {
  margin: 0;
  font-size: 34px;
  line-height: 1.2;
}

.meta {
  margin: 14px 0 0;
  color: #61708a;
}

.refresh-button {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  min-height: 44px;
  padding: 0 18px;
  color: #ffffff;
  background: #172033;
  border: 0;
  border-radius: 8px;
  cursor: pointer;
}

.dashboard-body {
  display: grid;
  grid-template-columns: 280px minmax(0, 1fr);
  gap: 24px;
  padding: 24px;
}

.sidebar {
  display: flex;
  flex-direction: column;
  gap: 10px;
  min-height: calc(100vh - 150px);
  padding: 16px;
  background: #ffffff;
  border: 1px solid #cfdae8;
  border-radius: 8px;
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 6px;
  width: 100%;
  padding: 16px;
  color: #172033;
  background: transparent;
  border: 0;
  border-radius: 8px;
  cursor: pointer;
}

.nav-item span {
  font-weight: 800;
}

.nav-item small {
  color: #61708a;
}

.nav-item.active {
  color: #ffffff;
  background: #172033;
}

.nav-item.active small {
  color: #d9e4f2;
}

.content {
  min-width: 0;
}

.overview-panel {
  margin-bottom: 18px;
  padding: 20px;
  background: #ffffff;
  border: 1px solid #cfdae8;
  border-radius: 8px;
}

.overview-panel h2 {
  margin: 0 0 10px;
}

.overview-panel p,
.overview-panel li {
  color: #61708a;
  line-height: 1.7;
}

.indicator-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
  gap: 18px;
}

.indicator-card {
  min-width: 0;
  padding: 20px;
  background: #ffffff;
  border: 1px solid #cfdae8;
  border-radius: 8px;
}

.card-topline {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  color: #61708a;
}

.card-topline span {
  color: #172033;
  font-weight: 800;
}

.metric-row {
  display: flex;
  align-items: baseline;
  gap: 8px;
  margin: 14px 0;
}

.metric-row strong {
  font-size: 36px;
  line-height: 1;
}

.metric-row span,
.metric-row em {
  color: #61708a;
  font-style: normal;
  font-weight: 700;
}

.metric-row .up {
  color: #d12b2b;
}

.metric-row .down {
  color: #07856f;
}

.chart-box {
  height: 240px;
  overflow: hidden;
  border: 1px solid #e3ebf4;
  border-radius: 8px;
}

.reading {
  min-height: 72px;
  margin: 14px 0 0;
  color: #61708a;
  line-height: 1.7;
}

.state-panel {
  margin: 24px;
  padding: 24px;
  color: #61708a;
  background: #ffffff;
  border: 1px solid #cfdae8;
  border-radius: 8px;
}

@media (max-width: 900px) {
  .dashboard-header {
    align-items: flex-start;
    flex-direction: column;
  }

  .dashboard-body {
    grid-template-columns: 1fr;
  }

  .sidebar {
    min-height: 0;
  }
}
```

- [ ] **Step 8: Run frontend build**

Run:

```powershell
cd frontend
npm install
npm run build
```

Expected:

```text
vite build ...
✓ built
```

- [ ] **Step 9: Run local visual smoke test**

Run backend:

```powershell
python -m backend.cli init-db
python -m backend.cli ingest --provider seed
uvicorn backend.app:create_app --factory --host 127.0.0.1 --port 8000
```

Run frontend in another shell:

```powershell
cd frontend
npm run dev -- --host 127.0.0.1 --port 5173
```

Open:

```text
http://127.0.0.1:5173
```

Expected:

- Header shows `全球宏观监测器`.
- Sidebar shows the six requested domains.
- Rates page shows cards; seed-backed pages show cards after running seed ingestion.
- No text overlaps at desktop width or mobile width.

- [ ] **Step 10: Commit if git is initialized**

```powershell
git add frontend
git commit -m "feat: add macro dashboard frontend"
```

## Task 7: Quality Gate And Progress Log

**Files:**
- Modify: `E:\code\finance\PREGRESS.md`
- Modify: `E:\code\finance\README.md`

- [ ] **Step 1: Run full backend checks**

Run:

```powershell
ruff check backend tests
pytest -q
```

Expected:

```text
All checks passed
8 passed
```

- [ ] **Step 2: Run full frontend checks**

Run:

```powershell
cd frontend
npm run build
```

Expected:

```text
✓ built
```

- [ ] **Step 3: Update progress log**

Append to `PREGRESS.md`:

```markdown
## 2026-05-21

### 进展

- 初始化本地宏观数据监控项目。
- 建立指标目录、DuckDB 存储、FRED/seed 采集、FastAPI API 和 React 仪表盘。
- MVP 已覆盖国债利率、各国经济、有色、原油、煤炭、电力的领域入口。

### 教训

- 先用统一指标目录和种子数据打通链路，可以降低一次性接入多个不稳定数据源的风险。
- 真实爬虫应按主题逐个替换 seed provider，保持接口不变。

### 提交记录

- `feat: bootstrap macro monitor project`
- `feat: add macro indicator catalog`
- `feat: add duckdb macro storage`
- `feat: add macro ingestion providers`
- `feat: expose macro api and cli`
- `feat: add macro dashboard frontend`

### TODO

- 接入中国宏观官方数据或 Wind。
- 接入 EIA / FRED 能源数据。
- 接入 LME/SHFE 库存和产能指标。
- 增加调度任务和数据质量告警。
```

- [ ] **Step 4: Update README next steps**

Append to `README.md`:

```markdown
## 后续数据源优先级

1. 国债利率：扩展中国、德国、日本收益率曲线。
2. 国家宏观：GDP、财政赤字、政府债务、CPI、PPI、PMI。
3. 有色：LME/SHFE 库存、价格、加工费、产能。
4. 原油：Brent/WTI、EIA 库存、炼厂开工、成品油裂解、油运费率。
5. 煤炭：港口价格、库存、日耗、进口。
6. 电力：发电量、用电量、火电水电风光分项、煤耗。
```

- [ ] **Step 5: Commit if git is initialized**

```powershell
git add README.md PREGRESS.md
git commit -m "docs: record macro monitor progress"
```

## Self-Review

Spec coverage:

- 国债利率: covered by FRED Treasury catalog, provider, API, and dashboard.
- 各国经济: covered by country macro catalog and seed provider; real adapters are intentionally deferred behind the provider interface.
- 有色板块: covered by nonferrous catalog and seed provider.
- 原油板块: covered by crude oil catalog and seed provider.
- 煤炭板块: covered by coal catalog and seed provider.
- 电力板块: covered by power catalog and seed provider.
- 其他拓展: covered by indicator catalog and provider protocol.
- Screenshot-inspired layout: covered by frontend header/sidebar/card/chart layout.

Placeholder scan:

- No implementation step depends on an undefined function without defining it in an earlier task.
- Real third-party data sources beyond FRED are deferred explicitly to later plans and still have working seed data in this MVP.

Type consistency:

- Backend response model fields match frontend TypeScript types.
- `IndicatorDefinition`, `Observation`, and `IndicatorSnapshot` are used consistently across storage, API, and frontend.

## Execution Options

Plan complete and saved to `docs/superpowers/plans/2026-05-21-local-macro-monitor.md`. Two execution options:

1. Subagent-Driven (recommended) - dispatch a fresh subagent per task, review between tasks, fast iteration.
2. Inline Execution - execute tasks in this session using executing-plans, batch execution with checkpoints.

Which approach?
