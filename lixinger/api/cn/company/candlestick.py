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
    type_: Literal["ex_rights", "lxr_fc_rights", "fc_rights", "bc_rights"],
    start_date: str,
    stock_code: str,
    end_date: str | None = None,
    adjust_forward_date: str | None = None,
    adjust_backward_date: str | None = None,
    limit: int | None = None,
) -> pa.typing.DataFrame[Output]:
    """获取K线数据.

    参考文档: https://www.lixinger.com/open/api/doc?api-key=cn/company/candlestick
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
    if adjust_forward_date is not None:
        payload["adjustForwardDate"] = adjust_forward_date
    if adjust_backward_date is not None:
        payload["adjustBackwardDate"] = adjust_backward_date

    response = client.post(
        f"{settings.base_url}/cn/company/candlestick",
        json=payload,
    )
    df = get_response_df(response, Output)
    return df
