from __future__ import annotations

import pandera as pa
import requests
from pydantic import validate_arguments

from lixinger.config import settings
from lixinger.utils import adjust_request_date_range, get_response_df


class Output(pa.DataFrameModel):
    date: pa.typing.Series[pa.typing.DateTime]
    trading_price: pa.typing.Series[float]
    trading_money: pa.typing.Series[float]
    trading_volume: pa.typing.Series[float]
    buy_branch: pa.typing.Series[str]
    sell_branch: pa.typing.Series[str]
    special: pa.typing.Series[str] = pa.Field(nullable=True)


@validate_arguments
@pa.check_types
@adjust_request_date_range
def get_block_deal(
    start_date: str,
    stock_code: str,
    end_date: str | None = None,
    limit: int | None = None,
) -> pa.typing.DataFrame[Output]:
    """获取大宗交易数据.

    参考文档: https://www.lixinger.com/open/api/doc?api-key=cn/company/block-deal
    """
    payload = {
        "token": settings.token,
        "startDate": start_date,
        "stockCode": stock_code,
    }
    if end_date is not None:
        payload["endDate"] = end_date
    if limit is not None:
        payload["limit"] = limit

    response = requests.post(
        f"{settings.base_url}/cn/company/block-deal",
        json=payload,
    )
    df = get_response_df(response, Output)
    return df
