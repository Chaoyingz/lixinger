from lixinger.api.cn.company.fundamental_non_financial import (
    get_fundamental_non_financial,
)


def test_fundamental_non_financial() -> None:
    get_fundamental_non_financial(
        stock_codes=["600519"], metrics_list=["pe_ttm"], start_date="2010-01-01"
    )
