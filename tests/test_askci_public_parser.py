"""中商公开数据页解析测试。"""

from decimal import Decimal

from backend.domain.catalog import get_indicator
from backend.ingest.askci_public import parse_askci_monthly_output_table


def test_parse_askci_monthly_output_table_extracts_monthly_value() -> None:
    html = """
    <table class="fancyTable" id="myTable03">
      <thead>
        <tr>
          <th></th><th>日期</th><th>当月产量(亿千瓦时)</th>
          <th>累计产量(亿千瓦时)</th><th>当月同比增长(%)</th><th>累计增长(%)</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="tab_fwit">1</td><td>2025年12月</td><td>5811.7</td>
          <td>62945.5</td><td>-3.2</td><td>-1</td>
        </tr>
      </tbody>
    </table>
    """

    observations = parse_askci_monthly_output_table(
        html=html,
        indicator=get_indicator("CN_THERMAL_POWER_GENERATION"),
        source="中商产业研究院/NBS:a03010h",
        value_kind="monthly_value",
    )

    assert len(observations) == 1
    assert observations[0].period.isoformat() == "2025-12-01"
    assert observations[0].value == Decimal("5811.7")
    assert observations[0].provider == "askci_public"


def test_parse_askci_monthly_output_table_extracts_yoy() -> None:
    html = """
    <table class="fancyTable" id="myTable03">
      <tbody>
        <tr>
          <td>1</td><td>2025年12月</td><td>1041.4</td>
          <td>10530.8</td><td>8.9</td><td>9.7</td>
        </tr>
      </tbody>
    </table>
    """

    observations = parse_askci_monthly_output_table(
        html=html,
        indicator=get_indicator("CN_WIND_POWER_GENERATION"),
        source="中商产业研究院/NBS:a03010k",
        value_kind="monthly_yoy",
    )

    assert observations[0].period.isoformat() == "2025-12-01"
    assert observations[0].value == Decimal("8.9")
