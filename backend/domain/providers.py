"""数据源适配器接口。"""

from typing import Protocol

from backend.domain.models import IndicatorDefinition, Observation


class MacroDataProvider(Protocol):
    """宏观数据源适配器协议。"""

    name: str

    def supports(self, indicator: IndicatorDefinition) -> bool:
        """判断当前适配器是否支持该指标。"""

    async def fetch(self, indicator: IndicatorDefinition) -> list[Observation]:
        """拉取指标观测值。"""

