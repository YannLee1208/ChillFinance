"""测试公共配置。"""

from collections.abc import Iterator
from pathlib import Path

import pytest


@pytest.fixture()
def temp_db_path(tmp_path: Path) -> Iterator[Path]:
    """提供临时 DuckDB 路径。"""

    yield tmp_path / "macro.duckdb"
