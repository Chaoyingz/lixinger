from lixinger.api.cn.company.shareholders_num import get_shareholders_num


def test_shareholders_num() -> None:
    get_shareholders_num(start_date="2021-01-01", stock_code="600519")
