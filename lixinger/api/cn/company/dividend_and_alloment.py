from __future__ import annotations

import numpy as np
import pandas as pd
import pandera as pa
import requests
from pydantic import validate_arguments

from lixinger.config import settings
from lixinger.utils import get_response_df


class Output(pa.DataFrameModel):
    date: pa.typing.Series[pa.typing.DateTime]
    bonus_shares_from_profit: pa.typing.Series[int]
    bonus_shares_from_capital_reserve: pa.typing.Series[int]
    dividend: pa.typing.Series[float]
    content: pa.typing.Series[str] = pa.Field(nullable=True)
    register_date: pa.typing.Series[pa.typing.DateTime] = pa.Field(nullable=True)
    ex_date: pa.typing.Series[pa.typing.DateTime] = pa.Field(nullable=True)
    payment_date: pa.typing.Series[pa.typing.DateTime] = pa.Field(nullable=True)
    status: pa.typing.Series[str]
    original_value: pa.typing.Series[float]
    split_ratio: pa.typing.Series[float] = pa.Field(nullable=True)


@validate_arguments
@pa.check_types
def get_dividend_and_alloment(
    start_date: str,
    stock_code: str,
    end_date: str | None = None,
    limit: int | None = None,
) -> pa.typing.DataFrame[Output]:
    """获取分红送配信息.

    参考文档: https://www.lixinger.com/open/api/doc?api-key=cn/company/dividend-and-alloment
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
        f"{settings.base_url}/cn/company/dividend-and-alloment",
        json=payload,
    )
    df = get_response_df(response)
    df["date"] = pd.to_datetime(df["date"]).dt.tz_localize(None) + pd.Timedelta("8h")
    df["register_date"] = pd.to_datetime(df["register_date"]).dt.tz_localize(None)
    df["ex_date"] = pd.to_datetime(df["ex_date"]).dt.tz_localize(None) + pd.Timedelta(
        "8h"
    )
    if "content" not in df.columns:
        df["content"] = np.nan
    if "payment_date" not in df.columns:
        df["payment_date"] = np.nan
    df["payment_date"] = pd.to_datetime(df["payment_date"]).dt.tz_localize(None)
    if "split_ratio" not in df.columns:
        df["split_ratio"] = np.nan
    return df
