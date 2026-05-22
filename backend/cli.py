"""命令行入口。"""

import asyncio

import typer

from backend.config import get_settings
from backend.domain.catalog import get_catalog
from backend.ingest.akshare_china import AkShareChinaProvider
from backend.ingest.china_data import ChinaDataProvider
from backend.ingest.coal_public import CoalPublicProvider
from backend.ingest.fred import FredSeriesProvider
from backend.ingest.seed import SeedProvider
from backend.ingest.service import IngestionService
from backend.ingest.unavailable import UnavailableProvider
from backend.ingest.us_treasury import USTreasuryProvider
from backend.ingest.world_bank import WorldBankProvider
from backend.storage.duckdb_store import DuckDBMacroStore

app = typer.Typer(help="Local macro monitor commands.")
_VALID_PROVIDERS = {
    "akshare_china",
    "china_data",
    "coal_public",
    "fred",
    "seed",
    "unavailable",
    "us_treasury",
    "world_bank",
}


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
        help="Provider name: fred, world_bank, or seed.",
    ),
    codes: str | None = typer.Option(
        default=None,
        help="Comma-separated indicator codes to ingest.",
    ),
) -> None:
    """从数据源采集观测值并写入本地数据库。"""

    provider_name = _validate_provider_name(provider)
    requested_codes = _parse_codes(codes)
    settings = get_settings()
    store = DuckDBMacroStore(settings.macro_db_path)
    store.initialize()
    service = IngestionService(
        store=store,
        providers=[
            AkShareChinaProvider(),
            USTreasuryProvider(
                timeout_seconds=settings.macro_http_timeout_seconds,
                user_agent=settings.macro_user_agent,
            ),
            ChinaDataProvider(
                timeout_seconds=settings.macro_http_timeout_seconds,
                user_agent=settings.macro_user_agent,
            ),
            CoalPublicProvider(
                timeout_seconds=settings.macro_http_timeout_seconds,
                user_agent=settings.macro_user_agent,
            ),
            FredSeriesProvider(
                timeout_seconds=settings.macro_http_timeout_seconds,
                user_agent=settings.macro_user_agent,
            ),
            WorldBankProvider(
                timeout_seconds=settings.macro_http_timeout_seconds,
                user_agent=settings.macro_user_agent,
            ),
            UnavailableProvider(),
            SeedProvider(),
        ],
    )

    indicators = [
        indicator
        for indicator in get_catalog()
        if requested_codes is None or indicator.code in requested_codes
    ]
    result = asyncio.run(service.ingest(indicators, provider_name=provider_name))
    typer.echo(f"Ingested observations: {result.observation_count}")
    if result.failed_indicators:
        typer.echo(f"Failed indicators: {len(result.failed_indicators)}")
        for code, reason in result.failed_indicators.items():
            typer.echo(f"- {code}: {reason}")


def _validate_provider_name(provider: str | None) -> str | None:
    if provider is None or provider in _VALID_PROVIDERS:
        return provider

    raise typer.BadParameter(
        "Provider name must be one of: akshare_china, china_data, coal_public, fred, seed, "
        "unavailable, us_treasury, world_bank"
    )


def _parse_codes(codes: str | None) -> set[str] | None:
    if codes is None:
        return None
    parsed = {code.strip() for code in codes.split(",") if code.strip()}
    return parsed or None


if __name__ == "__main__":
    app()
