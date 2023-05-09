from lixinger.api.cn.company.indices import get_indices


def test_get_indices() -> None:
    get_indices(stock_code="600519")
