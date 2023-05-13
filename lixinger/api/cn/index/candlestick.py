from __future__ import annotations

from typing import Literal

import pandera as pa

from lixinger import client
from lixinger.config import settings
from lixinger.utils import api, get_response_df


class Output(pa.DataFrameModel):
    date: pa.typing.Series[pa.typing.DateTime]
    open: pa.typing.Series[float]
    high: pa.typing.Series[float]
    low: pa.typing.Series[float]
    close: pa.typing.Series[float]
    volume: pa.typing.Series[int]
    amount: pa.typing.Series[int]
    change: pa.typing.Series[float]


@api
def get_candlestick(
    type_: Literal["normal", "total_return"],
    start_date: str,
    stock_code: str,
    end_date: str | None = None,
    limit: int | None = None,
) -> pa.typing.DataFrame[Output]:
    """获取K线数据.

    参考文档: https://www.lixinger.com/open/api/doc?api-key=cn/index/candlestick
    """
    payload = {
        "type": type_,
        "token": settings.token,
        "startDate": start_date,
        "stockCode": stock_code,
    }
    if end_date is not None:
        payload["endDate"] = end_date
    if limit is not None:
        payload["limit"] = limit

    response = client.post(
        f"{settings.base_url}/cn/index/candlestick",
        json=payload,
    )
    df = get_response_df(response, Output)
    return df
