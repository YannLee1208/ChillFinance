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
