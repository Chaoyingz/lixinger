from __future__ import annotations

import pandera as pa
import requests
from pydantic import validate_arguments

from lixinger.config import settings
from lixinger.utils import adjust_request_date_range, get_response_df


class Output(pa.DataFrameModel):
    date: pa.typing.Series[pa.typing.DateTime]
    pledgor: pa.typing.Series[str] = pa.Field(nullable=True)
    pledgee: pa.typing.Series[str] = pa.Field(nullable=True)
    pledge_matters: pa.typing.Series[str] = pa.Field(nullable=True)
    pledge_shares_nature: pa.typing.Series[str] = pa.Field(nullable=True)
    pledge_amount: pa.typing.Series[float] = pa.Field(nullable=True)
    pledge_percentage_of_total_equity: pa.typing.Series[float] = pa.Field(nullable=True)
    pledge_start_date: pa.typing.Series[pa.typing.DateTime] = pa.Field(nullable=True)
    pledge_end_date: pa.typing.Series[pa.typing.DateTime] = pa.Field(nullable=True)
    pledge_discharge_date: pa.typing.Series[pa.typing.DateTime] = pa.Field(
        nullable=True
    )
    pledge_discharge_explanation: pa.typing.Series[str] = pa.Field(nullable=True)
    pledge_discharge_amount: pa.typing.Series[float] = pa.Field(nullable=True)
    is_pledge_repurchase_transactions: pa.typing.Series[bool] = pa.Field(nullable=True)
    accumulated_pledge_percentage_of_total_equity: pa.typing.Series[float] = pa.Field(
        nullable=True
    )


@validate_arguments
@pa.check_types
@adjust_request_date_range
def get_pledge(
    start_date: str,
    stock_code: str,
    end_date: str | None = None,
    limit: int | None = None,
) -> pa.typing.DataFrame[Output]:
    """获取股权质押数据.

    参考文档: https://www.lixinger.com/open/api/doc?api-key=cn/company/pledge
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
        f"{settings.base_url}/cn/company/block-deal",
        json=payload,
    )
    df = get_response_df(response, Output)
    return df
