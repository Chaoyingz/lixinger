from lixinger.api.cn.company.senior_executive_shares_change import (
    get_senior_executive_shares_change,
)


def test_shareholders_num() -> None:
    get_senior_executive_shares_change(start_date="2021-01-01", stock_code="300390")
