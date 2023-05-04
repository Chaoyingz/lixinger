from __future__ import annotations

import pandas as pd
import pandera as pa
import requests
from pydantic import validate_arguments

from lixinger.config import settings
from lixinger.utils import get_response_df


class Output(pa.DataFrameModel):
    date: pa.typing.Series[pa.typing.DateTime]
    total_net_value: pa.typing.Series[float]


@validate_arguments
@pa.check_types
def get_total_net_value(
    *,
    start_date: str,
    end_date: str | None = None,
    limit: int | None = None,
    stock_code: str,
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

    response = requests.post(
        f"{settings.base_url}/cn/fund/total-net-value",
        json=payload,
    )
    df = get_response_df(response)
    df["date"] = pd.to_datetime(df["date"]).dt.tz_localize(None)
    return df
