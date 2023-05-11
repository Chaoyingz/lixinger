from lixinger.api.cn.index.base import get_index


def test_get_index() -> None:
    get_index(stock_codes=["000016"])
