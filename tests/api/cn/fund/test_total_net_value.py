from lixinger.api.cn.fund.total_net_value import get_total_net_value


def test_get_index_fundamental():
    get_total_net_value(
        start_date="2023-04-20",
        end_date="2023-04-30",
        stock_code="163406",
    )
