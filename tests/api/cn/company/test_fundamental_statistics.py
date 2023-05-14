from lixinger.api.cn.company.fundamental_statistics import (
    get_fundamental_statistics,
)


def test_fundamental_statistics() -> None:
    get_fundamental_statistics(
        stock_codes=["300750", "600519"], granularity="y3", metrics_list=["pe_ttm"]
    )
