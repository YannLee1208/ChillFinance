"""CLI 测试。"""

from typer.testing import CliRunner

from backend.cli import app


def test_ingest_rejects_unknown_provider() -> None:
    runner = CliRunner()

    result = runner.invoke(app, ["ingest", "--provider", "invalid"])

    assert result.exit_code != 0
    assert "Provider name must be one of: seed, fred" in result.output
