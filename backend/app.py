"""FastAPI 应用入口。"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.config import get_settings
from backend.domain.catalog import get_catalog, get_indicator
from backend.domain.models import IndicatorDefinition, IndicatorSnapshot, Observation
from backend.storage.duckdb_store import DuckDBMacroStore

_ALLOWED_ORIGINS = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
]


def create_app() -> FastAPI:
    """创建本地宏观监控 API 应用。"""

    api = FastAPI(title="Local Macro Monitor")
    api.add_middleware(
        CORSMiddleware,
        allow_origins=_ALLOWED_ORIGINS,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @api.get("/health")
    def health() -> dict[str, str]:
        """返回服务健康状态。"""

        return {"status": "ok"}

    @api.get("/api/catalog", response_model=list[IndicatorDefinition])
    def catalog() -> list[IndicatorDefinition]:
        """返回指标目录。"""

        return get_catalog()

    @api.get("/api/indicators/{indicator_code}", response_model=IndicatorSnapshot)
    def indicator_snapshot(indicator_code: str) -> IndicatorSnapshot:
        """返回单个指标的定义、最新值、前值和完整序列。"""

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

    @api.get("/api/observations/{indicator_code}", response_model=list[Observation])
    def observations(indicator_code: str) -> list[Observation]:
        """返回单个指标的观测序列。"""

        settings = get_settings()
        store = DuckDBMacroStore(settings.macro_db_path)
        store.initialize()
        return store.get_series(indicator_code)

    return api
