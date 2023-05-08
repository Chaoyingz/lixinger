from lixinger.api.cn.company.block_deal import get_block_deal


def test_get_block_deal() -> None:
    get_block_deal(start_date="2021-01-01", stock_code="600519")
