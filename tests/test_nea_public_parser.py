"""国家能源局公开页面解析测试。"""

from decimal import Decimal

from backend.domain.catalog import get_indicator
from backend.ingest.nea_public import parse_nea_electricity_article


def test_parse_nea_electricity_article_extracts_monthly_consumption() -> None:
    html = """
    <html>
      <head>
        <meta name="ArticleTitle" content="2026年4月份全社会用电量同比增长6.0%">
      </head>
      <body>
        <p>5月19日，国家能源局发布4月份全社会用电量等数据。</p>
        <p>4月份，全社会用电量8205亿千瓦时，同比增长6.0%。从分产业用电看，
        第一产业用电量112亿千瓦时，同比增长2.0%。第二产业用电量5584亿千瓦时，
        同比增长5.3%；其中，工业用电量5538亿千瓦时，同比增长5.5%。第三产业用电量
        1517亿千瓦时，同比增长8.9%。城乡居民生活用电量992亿千瓦时，同比增长6.0%。</p>
        <p>1～4月，全社会用电量累计33345亿千瓦时，同比增长5.4%。</p>
      </body>
    </html>
    """

    observations = parse_nea_electricity_article(
        html=html,
        indicator=get_indicator("CN_SECONDARY_INDUSTRY_ELECTRICITY"),
        source="国家能源局:2026年4月份全社会用电量同比增长6.0%",
    )

    assert len(observations) == 1
    assert observations[0].period.isoformat() == "2026-04-01"
    assert observations[0].value == Decimal("5584")
    assert observations[0].provider == "nea_public"


def test_parse_nea_electricity_article_extracts_yoy() -> None:
    html = """
    <html>
      <head>
        <meta name="ArticleTitle" content="2026年4月份全社会用电量同比增长6.0%">
      </head>
      <body>
        <p>4月份，全社会用电量8205亿千瓦时，同比增长6.0%。从分产业用电看，
        第一产业用电量112亿千瓦时，同比增长2.0%。第二产业用电量5584亿千瓦时，
        同比增长5.3%。第三产业用电量1517亿千瓦时，同比增长8.9%。城乡居民生活用电量
        992亿千瓦时，同比增长6.0%。</p>
      </body>
    </html>
    """

    observations = parse_nea_electricity_article(
        html=html,
        indicator=get_indicator("CN_TERTIARY_INDUSTRY_ELECTRICITY_YOY"),
        source="国家能源局:2026年4月份全社会用电量同比增长6.0%",
    )

    assert len(observations) == 1
    assert observations[0].period.isoformat() == "2026-04-01"
    assert observations[0].value == Decimal("8.9")
