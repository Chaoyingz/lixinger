from __future__ import annotations

from typing import Literal

import pandera as pa

from lixinger import client
from lixinger.config import settings
from lixinger.utils import api, get_response_df


class Output(pa.DataFrameModel):
    date: pa.typing.Series[pa.typing.DateTime]
    value: pa.typing.Series[float]


@api
def get_index_drawdown(
    start_date: str,
    stock_code: str,
    granularity: Literal["m", "q", "hy", "y"],
    end_date: str | None = None,
) -> pa.typing.DataFrame[Output]:
    """获取指数回撤数据.

    参考文档: https://www.lixinger.com/open/api/doc?api-key=cn/index/drawdown
    """
    payload = {
        "token": settings.token,
        "startDate": start_date,
        "stockCode": stock_code,
        "granularity": granularity,
    }
    if end_date is not None:
        payload["endDate"] = end_date
    response = client.post(
        f"{settings.base_url}/cn/index/drawdown",
        json=payload,
    )
    return get_response_df(response, Output)
