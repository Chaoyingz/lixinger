from lixinger.api.cn.company.industries import get_industries


def test_get_industries() -> None:
    get_industries(stock_code="600519")
