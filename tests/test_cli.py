"""CLI 测试。"""

from typer.testing import CliRunner

from backend.cli import _parse_codes, app


def test_ingest_rejects_unknown_provider() -> None:
    runner = CliRunner()

    result = runner.invoke(app, ["ingest", "--provider", "invalid"])

    assert result.exit_code != 0
    assert "Provider name must be one of:" in result.output
    assert "china_data" in result.output
    assert "eia_public" in result.output


def test_parse_codes_splits_comma_separated_values() -> None:
    assert _parse_codes("US_DGS10, CN_GDP,") == {"US_DGS10", "CN_GDP"}
    assert _parse_codes(None) is None
