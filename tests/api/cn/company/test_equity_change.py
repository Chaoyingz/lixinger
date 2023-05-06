from lixinger.api.cn.company.equity_change import get_equity_change


def test_get_company() -> None:
    get_equity_change(start_date="2013-01-01", stock_code="600519")
