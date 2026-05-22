"""国家能源局公开页面数据适配器。"""

import html
import re
from datetime import UTC, date, datetime
from decimal import Decimal, InvalidOperation
from typing import Any
from urllib.parse import urljoin

import httpx

from backend.constant import NEA_PUBLIC_SERIES
from backend.domain.models import IndicatorDefinition, Observation

_NEA_HOME_URL = "https://www.nea.gov.cn/"
_NUMBER_PATTERN = r"[-+]?\d+(?:\.\d+)?"

_METRIC_PATTERNS = {
    "total": (
        rf"\d{{1,2}}月份，全社会用电量(?P<value>{_NUMBER_PATTERN})亿千瓦时，"
        rf"同比增长(?P<yoy>{_NUMBER_PATTERN})%"
    ),
    "primary": (
        rf"第一产业用电量(?P<value>{_NUMBER_PATTERN})亿千瓦时，"
        rf"同比增长(?P<yoy>{_NUMBER_PATTERN})%"
    ),
    "secondary": (
        rf"第二产业用电量(?P<value>{_NUMBER_PATTERN})亿千瓦时，"
        rf"同比增长(?P<yoy>{_NUMBER_PATTERN})%"
    ),
    "tertiary": (
        rf"第三产业用电量(?P<value>{_NUMBER_PATTERN})亿千瓦时，"
        rf"同比增长(?P<yoy>{_NUMBER_PATTERN})%"
    ),
    "residential": (
        rf"城乡居民生活用电量(?P<value>{_NUMBER_PATTERN})亿千瓦时，"
        rf"同比增长(?P<yoy>{_NUMBER_PATTERN})%"
    ),
}


class NEAPublicProvider:
    """从国家能源局官网拉取最新全社会用电量公开数据。"""

    name = "nea_public"

    def __init__(
        self,
        timeout_seconds: int = 20,
        user_agent: str = "local-macro-monitor/0.1",
    ) -> None:
        self.timeout_seconds = timeout_seconds
        self.user_agent = user_agent
        self._latest_article_cache: tuple[str, str] | None = None

    def supports(self, indicator: IndicatorDefinition) -> bool:
        """判断指标是否配置了国家能源局公开页面。"""

        return indicator.provider == self.name and indicator.code in NEA_PUBLIC_SERIES

    async def fetch(self, indicator: IndicatorDefinition) -> list[Observation]:
        """下载国家能源局最新用电量文章并转换为统一观察值。"""

        html_text, source = await self._fetch_latest_electricity_article()
        return parse_nea_electricity_article(
            html=html_text,
            indicator=indicator,
            source=source,
        )

    async def _fetch_latest_electricity_article(self) -> tuple[str, str]:
        if self._latest_article_cache is not None:
            return self._latest_article_cache

        headers = {"User-Agent": self.user_agent}
        async with httpx.AsyncClient(
            timeout=self.timeout_seconds,
            headers=headers,
            follow_redirects=True,
        ) as client:
            home_response = await client.get(_NEA_HOME_URL)
            home_response.raise_for_status()
            article_url, article_title = find_latest_electricity_article(
                home_response.text,
                base_url=_NEA_HOME_URL,
            )
            article_response = await client.get(article_url)
            article_response.raise_for_status()

        source = f"国家能源局:{article_title}:{article_url}"
        self._latest_article_cache = (article_response.text, source)
        return self._latest_article_cache


def find_latest_electricity_article(
    html_text: str,
    base_url: str = _NEA_HOME_URL,
) -> tuple[str, str]:
    """从国家能源局首页找出最新全社会用电量文章链接。"""

    pattern = re.compile(r'<a\s+href="(?P<href>[^"]+)"[^>]*>(?P<title>[^<]+)</a>')
    candidates: list[tuple[str, str]] = []
    for match in pattern.finditer(html_text):
        title = html.unescape(match.group("title")).strip()
        if "全社会用电量" not in title or "月份" not in title:
            continue
        candidates.append((urljoin(base_url, match.group("href")), title))

    if not candidates:
        raise ValueError("国家能源局首页未找到全社会用电量月度文章")
    return candidates[0]


def parse_nea_electricity_article(
    *,
    html: str,
    indicator: IndicatorDefinition,
    source: str,
) -> list[Observation]:
    """解析国家能源局全社会用电量文章中的当月数据。"""

    config = NEA_PUBLIC_SERIES[indicator.code]
    text = _html_to_text(html)
    period = _parse_article_period(text)
    metric = config["metric"]
    kind = config["kind"]
    pattern = _METRIC_PATTERNS[metric]
    match = re.search(pattern, text)
    if match is None:
        raise ValueError(f"国家能源局文章缺少 {metric} 用电量数据")

    return [
        Observation(
            indicator_code=indicator.code,
            period=period,
            value=_to_decimal(match.group(kind)),
            provider=NEAPublicProvider.name,
            source=source,
            ingested_at=datetime.now(UTC),
        )
    ]


def _html_to_text(html_text: str) -> str:
    meta_values = " ".join(
        html.unescape(match.group(1))
        for match in re.finditer(r'<meta[^>]+content="([^"]+)"', html_text, flags=re.IGNORECASE)
    )
    without_scripts = re.sub(
        r"<(script|style)[^>]*>.*?</\1>",
        "",
        html_text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    without_tags = re.sub(r"<[^>]+>", " ", without_scripts)
    text = f"{meta_values} {html.unescape(without_tags)}"
    return re.sub(r"\s+", "", text)


def _parse_article_period(text: str) -> date:
    match = re.search(r"(?P<year>\d{4})年(?P<month>\d{1,2})月份全社会用电量", text)
    if match is None:
        raise ValueError("国家能源局文章标题缺少年月")
    return date(int(match.group("year")), int(match.group("month")), 1)


def _to_decimal(value: Any) -> Decimal:
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"国家能源局数值无效: {value}") from exc
