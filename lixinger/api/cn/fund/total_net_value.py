from __future__ import annotations

import pandera as pa

from lixinger import client
from lixinger.config import settings
from lixinger.utils import api, get_response_df


class Output(pa.DataFrameModel):
    date: pa.typing.Series[pa.typing.DateTime]
    total_net_value: pa.typing.Series[float]


@api
def get_total_net_value(
    start_date: str,
    stock_code: str,
    end_date: str | None = None,
    limit: int | None = None,
) -> pa.typing.DataFrame[Output]:
    """获取基金累计净值数据

    参考文档: https://www.lixinger.com/open/api/doc?api-key=cn/fund/total-net-value
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

    response = client.post(
        f"{settings.base_url}/cn/fund/total-net-value",
        json=payload,
    )
    df = get_response_df(response, Output)
    return df
