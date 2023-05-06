from lixinger.api.cn.company.candlestick import get_candlestick


def test_get_candlestick() -> None:
    get_candlestick(type_="ex_rights", start_date="2021-01-01", stock_code="600519")
