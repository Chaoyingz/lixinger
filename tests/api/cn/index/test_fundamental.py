from lixinger.api.cn.index.fundamental import get_index_fundamental


def test_get_index_fundamental():
    get_index_fundamental(
        start_date="2023-04-20",
        end_date="2023-04-30",
        stock_codes=["000300"],
        metrics_list=["pe_ttm.mcw"],
    )
