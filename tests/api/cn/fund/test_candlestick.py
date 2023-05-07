from lixinger.api.cn.index.candlestick import get_candlestick


def test_get_candlestick() -> None:
    get_candlestick(type_="normal", start_date="2021-01-01", stock_code="000300")
