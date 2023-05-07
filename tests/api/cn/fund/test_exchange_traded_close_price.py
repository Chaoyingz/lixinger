from lixinger.api.cn.fund.exchange_traded_close_price import (
    get_exchange_traded_close_price,
)


def test_get_exchange_traded_close_price() -> None:
    get_exchange_traded_close_price(start_date="2021-01-01", stock_code="161725")
