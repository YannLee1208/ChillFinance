"""FRED 解析测试。"""

from decimal import Decimal
from subprocess import CompletedProcess

from backend.ingest import fred
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


def test_fetch_fred_csv_uses_system_curl(monkeypatch) -> None:
    calls: dict[str, object] = {}

    def fake_which(name: str) -> str | None:
        return "/usr/bin/curl" if name == "curl" else None

    def fake_run(args, **kwargs) -> CompletedProcess[str]:  # type: ignore[no-untyped-def]
        calls["args"] = args
        calls["kwargs"] = kwargs
        return CompletedProcess(args=args, returncode=0, stdout="DATE,DGS10\n", stderr="")

    monkeypatch.setattr(fred.shutil, "which", fake_which)
    monkeypatch.setattr(fred.subprocess, "run", fake_run)

    csv_text = fred._fetch_fred_csv(
        url="https://fred.stlouisfed.org/graph/fredgraph.csv",
        params={"id": "DGS10"},
        headers={"User-Agent": "test"},
        timeout_seconds=10,
    )

    assert csv_text == "DATE,DGS10\n"
    assert calls["args"][0] == "/usr/bin/curl"
    assert "--max-time" in calls["args"]
    assert calls["kwargs"]["timeout"] == 15
