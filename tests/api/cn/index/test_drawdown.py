from lixinger.api.cn.index.drawdown import get_index_drawdown


def test_get_index_drawdown():
    get_index_drawdown(
        start_date="2023-04-20",
        stock_code="000300",
        granularity="m",
    )
