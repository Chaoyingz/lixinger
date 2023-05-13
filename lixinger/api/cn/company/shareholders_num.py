from __future__ import annotations

import pandera as pa

from lixinger import client
from lixinger.config import settings
from lixinger.utils import api, get_response_df


class Output(pa.DataFrameModel):
    date: pa.typing.Series[pa.typing.DateTime]
    num: pa.typing.Series[int]


@api
def get_shareholders_num(
    start_date: str,
    stock_code: str,
    end_date: str | None = None,
    limit: int | None = None,
) -> pa.typing.DataFrame[Output]:
    """获取股东人数数据

    参考文档: https://www.lixinger.com/open/api/doc?api-key=cn/company/shareholders-num
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
        f"{settings.base_url}/cn/company/shareholders-num",
        json=payload,
    )
    df = get_response_df(response, Output)
    return df
