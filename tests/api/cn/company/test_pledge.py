from lixinger.api.cn.company.pledge import get_pledge


def test_pledge() -> None:
    get_pledge(start_date="2021-01-01", stock_code="000672")
