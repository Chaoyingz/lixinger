from __future__ import annotations

import pandera as pa
import requests
from pydantic import validate_arguments

from lixinger.config import settings
from lixinger.utils import adjust_request_date_range, get_response_df


class Output(pa.DataFrameModel):
    date: pa.typing.Series[pa.typing.DateTime]
    change_reason: pa.typing.Series[str]
    capitalization: pa.typing.Series[int]
    outstanding_shares_a: pa.typing.Series[int]
    limited_shares_a: pa.typing.Series[float] = pa.Field(nullable=True)


@validate_arguments
@pa.check_types
@adjust_request_date_range
def get_equity_change(
    start_date: str,
    stock_code: str,
    end_date: str | None = None,
    limit: int | None = None,
) -> pa.typing.DataFrame[Output]:
    """获取股本变动数据.

    参考文档: https://www.lixinger.com/open/api/doc?api-key=cn/company/equity-change
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
        f"{settings.base_url}/cn/company/equity-change",
        json=payload,
    )
    df = get_response_df(response, Output)
    return df
