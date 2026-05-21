"""宏观指标领域模型。"""

from datetime import date, datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field

Frequency = Literal["daily", "weekly", "monthly", "quarterly", "annual"]


class IndicatorDefinition(BaseModel):
    """指标定义。"""

    code: str
    name: str
    domain: str
    region: str
    unit: str
    frequency: Frequency
    provider: str
    source: str
    description: str
    display_order: int = 0


class Observation(BaseModel):
    """单个指标观测值。"""

    indicator_code: str
    period: date
    value: Decimal
    provider: str
    source: str
    ingested_at: datetime


class IndicatorSnapshot(BaseModel):
    """前端展示用指标快照。"""

    definition: IndicatorDefinition
    latest: Observation | None
    previous: Observation | None
    points: list[Observation] = Field(default_factory=list)

