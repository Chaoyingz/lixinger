from __future__ import annotations

import pandas as pd
import pandera as pa
import requests
from pydantic import validate_arguments

from lixinger.config import settings
from lixinger.utils import adjust_request_date_range, get_response_df


class Output(pa.DataFrameModel):
    date: pa.typing.Series[pa.typing.DateTime]
    open: pa.typing.Series[float]
    high: pa.typing.Series[float]
    low: pa.typing.Series[float]
    close: pa.typing.Series[float]


@validate_arguments
@pa.check_types
@adjust_request_date_range
def get_exchange_traded_close_price(
    start_date: str,
    stock_code: str,
    end_date: str | None = None,
    limit: int | None = None,
) -> pa.typing.DataFrame[Output]:
    """场内基金收盘价数据.

    参考文档: https://www.lixinger.com/open/api/doc?api-key=cn/fund/exchange-traded-close-price
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
        f"{settings.base_url}/cn/fund/exchange-traded-close-price",
        json=payload,
    )
    df = get_response_df(response, Output)
    df["date"] = pd.to_datetime(df["date"]).dt.tz_localize(None)
    return df
