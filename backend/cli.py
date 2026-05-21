"""命令行入口。"""

import asyncio

import typer

from backend.config import get_settings
from backend.domain.catalog import get_catalog
from backend.ingest.fred import FredTreasuryProvider
from backend.ingest.seed import SeedProvider
from backend.ingest.service import IngestionService
from backend.storage.duckdb_store import DuckDBMacroStore

app = typer.Typer(help="Local macro monitor commands.")
_VALID_PROVIDERS = {"seed", "fred"}


@app.command("init-db")
def init_db() -> None:
    """初始化本地 DuckDB 数据库并写入指标目录。"""

    settings = get_settings()
    store = DuckDBMacroStore(settings.macro_db_path)
    store.initialize()
    store.upsert_indicators(get_catalog())
    typer.echo(f"Initialized database: {settings.macro_db_path}")


@app.command()
def ingest(
    provider: str | None = typer.Option(
        default=None,
        help="Provider name: seed or fred.",
    ),
) -> None:
    """从数据源采集观测值并写入本地数据库。"""

    provider_name = _validate_provider_name(provider)
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

    total = asyncio.run(service.ingest(get_catalog(), provider_name=provider_name))
    typer.echo(f"Ingested observations: {total}")


def _validate_provider_name(provider: str | None) -> str | None:
    if provider is None or provider in _VALID_PROVIDERS:
        return provider

    raise typer.BadParameter("Provider name must be one of: seed, fred")


if __name__ == "__main__":
    app()
