from lixinger.api.cn.company.base import get_company


def test_get_company() -> None:
    get_company(stock_codes=["600519"])
