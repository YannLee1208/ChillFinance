"""确定性的种子数据适配器。"""

from datetime import UTC, date, datetime
from decimal import Decimal

from backend.domain.models import IndicatorDefinition, Observation

_SEED_VALUES: dict[str, list[tuple[date, Decimal]]] = {
    "CN_GDP_YOY": [
        (date(2025, 9, 30), Decimal("4.8")),
        (date(2025, 12, 31), Decimal("5.0")),
    ],
    "US_FISCAL_DEFICIT": [
        (date(2026, 1, 31), Decimal("-129")),
        (date(2026, 2, 28), Decimal("-236")),
    ],
    "EU_DEBT_TO_GDP": [
        (date(2025, 9, 30), Decimal("88.2")),
        (date(2025, 12, 31), Decimal("87.9")),
    ],
    "JP_GDP_YOY": [
        (date(2025, 9, 30), Decimal("1.4")),
        (date(2025, 12, 31), Decimal("1.1")),
    ],
    "CU_LME_INVENTORY": [
        (date(2026, 5, 1), Decimal("171000")),
        (date(2026, 5, 2), Decimal("169500")),
    ],
    "OIL_BRENT_PRICE": [
        (date(2026, 5, 1), Decimal("72.4")),
        (date(2026, 5, 2), Decimal("73.1")),
    ],
    "COAL_QHD_PRICE": [
        (date(2026, 4, 24), Decimal("712")),
        (date(2026, 5, 1), Decimal("719")),
    ],
    "CN_POWER_GENERATION": [
        (date(2026, 2, 28), Decimal("820")),
        (date(2026, 3, 31), Decimal("846")),
    ],
}


class SeedProvider:
    """返回内置种子数据的离线适配器。"""

    name = "seed"

    def supports(self, indicator: IndicatorDefinition) -> bool:
        """判断指标是否存在种子数据。"""

        return indicator.code in _SEED_VALUES

    async def fetch(self, indicator: IndicatorDefinition) -> list[Observation]:
        """返回指标对应的确定性种子观测值。"""

        ingested_at = datetime.now(UTC)
        return [
            Observation(
                indicator_code=indicator.code,
                period=period,
                value=value,
                provider=self.name,
                source=indicator.source,
                ingested_at=ingested_at,
            )
            for period, value in _SEED_VALUES[indicator.code]
        ]
