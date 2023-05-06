from lixinger.api.cn.company.dividend_and_alloment import (
    get_dividend_and_alloment,
)


def test_get_dividend_and_alloment() -> None:
    get_dividend_and_alloment(start_date="2021-01-01", stock_code="600519")
