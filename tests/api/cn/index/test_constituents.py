from lixinger.api.cn.index.constituents import get_index_constituents


def test_get_index_constituents():
    get_index_constituents(
        date="latest",
        stock_codes=["000016"],
    )
