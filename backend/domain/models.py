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
    selectors: dict[str, str] = Field(default_factory=dict)


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


class IngestionAttemptRecord(BaseModel):
    """单个指标采集尝试记录。"""

    run_id: str
    domain: str
    indicator_code: str
    provider: str
    status: str
    message: str
    observation_count: int
    started_at: datetime
    finished_at: datetime


class IngestionRunRecord(BaseModel):
    """一次板块采集运行记录。"""

    run_id: str
    domain: str
    status: str
    message: str
    observation_count: int
    success_count: int
    failure_count: int
    started_at: datetime
    finished_at: datetime
    attempts: list[IngestionAttemptRecord] = Field(default_factory=list)
