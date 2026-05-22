"""尚未稳定接入的数据源占位适配器。"""

from backend.constant import UNAVAILABLE_SERIES
from backend.domain.models import IndicatorDefinition, Observation


class UnavailableProvider:
    """把无法稳定公开抓取的指标转成前端可读的失败原因。"""

    name = "unavailable"

    def supports(self, indicator: IndicatorDefinition) -> bool:
        """判断指标是否属于待接入真实源的序列。"""

        return indicator.code in UNAVAILABLE_SERIES

    async def fetch(self, indicator: IndicatorDefinition) -> list[Observation]:
        """始终失败，但失败原因会被采集服务记录并展示在页面。"""

        reason = UNAVAILABLE_SERIES[indicator.code]
        raise RuntimeError(f"{reason}当前不会写入模拟数据。")
