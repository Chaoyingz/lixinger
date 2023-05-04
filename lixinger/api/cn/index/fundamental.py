from __future__ import annotations

import pandas as pd
import pandera as pa
import requests
from pydantic import validate_arguments

from lixinger.config import settings
from lixinger.utils import get_response_df


class Output(pa.DataFrameModel):
    date: pa.typing.Series[pa.typing.DateTime]
    stock_code: pa.typing.Series[str]


@validate_arguments
@pa.check_types
def get_index_fundamental(
    *,
    date: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    adjust_forward_date: str | None = None,
    adjust_backward_date: str | None = None,
    limit: int | None = None,
    stock_codes: list[str],
    metrics_list: list[str],
) -> pa.typing.DataFrame[Output]:
    """获取基本面数据，如PE、PB等.

    参考文档: https://www.lixinger.com/open/api/doc?api-key=cn/index/fundamental
    """
    payload = {
        "token": settings.token,
        "stockCodes": stock_codes,
        "metricsList": metrics_list,
    }
    if date is not None:
        payload["date"] = date
    if start_date is not None:
        payload["startDate"] = start_date
    if end_date is not None:
        payload["endDate"] = end_date
    if adjust_forward_date is not None:
        payload["adjustForwardDate"] = adjust_forward_date
    if adjust_backward_date is not None:
        payload["adjustBackwardDate"] = adjust_backward_date
    if limit is not None:
        payload["limit"] = limit
    response = requests.post(
        f"{settings.base_url}/cn/index/fundamental",
        json=payload,
    )
    df = get_response_df(response)
    df["date"] = pd.to_datetime(df["date"]).dt.tz_localize(None)
    df.sort_values(by=["date", "stock_code"], inplace=True)
    return df
