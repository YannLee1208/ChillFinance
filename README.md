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
| `EIA_API_KEY` | EIA API Key，用于后续接入原油库存、炼厂和成品油数据 | 空 |
| `WIND_API_KEY` | Wind API Key，用于后续替换中国宏观、LME/SHFE 等待接入指标 | 空 |
| `MACRO_HTTP_TIMEOUT_SECONDS` | HTTP 请求超时时间 | `60` |
| `MACRO_USER_AGENT` | 公共数据下载 User-Agent | `local-macro-monitor/0.1` |
| `VITE_API_BASE_URL` | 前端访问的后端地址 | `http://127.0.0.1:8000` |

## 本地开发

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
python -m backend.cli init-db
python -m backend.cli ingest
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
python -m ruff check backend tests
pytest -q
cd frontend
npm run build
```

## 后续数据源优先级

1. 国债利率：扩展中国、德国、日本收益率曲线。
2. 国家宏观：GDP、财政赤字、政府债务、CPI、PPI、PMI。
3. 有色：LME/SHFE 库存、价格、加工费、产能。
4. 原油：Brent/WTI、EIA 库存、炼厂开工、成品油裂解、油运费率。
5. 煤炭：港口价格、库存、日耗、进口。
6. 电力：发电量、用电量、火电水电风光分项、煤耗。

## 当前真实数据覆盖

- FRED：美国国债利率、日德欧长端利率、美国 GDP/债务/财政、原油、汽油、天然气、有色价格、煤炭价格、美国电力生产指数。
- World Bank：中日欧 GDP、债务占 GDP、财政余额占 GDP。
- seed provider 仅作为开发备用，不再出现在默认指标目录。
