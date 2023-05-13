from __future__ import annotations

import pandera as pa

from lixinger import client
from lixinger.config import settings
from lixinger.utils import api, get_response_df


class Output(pa.DataFrameModel):
    shareholder_name: pa.typing.Series[str]
    executive_name: pa.typing.Series[str]
    duty: pa.typing.Series[str]
    relation_between_e_s: pa.typing.Series[str]
    change_reason: pa.typing.Series[str]
    before_change_shares: pa.typing.Series[int]
    changed_shares: pa.typing.Series[int]
    after_change_shares: pa.typing.Series[int]
    avg_price: pa.typing.Series[float]


@api
def get_senior_executive_shares_change(
    start_date: str,
    stock_code: str,
    end_date: str | None = None,
    limit: int | None = None,
) -> pa.typing.DataFrame[Output]:
    """获取高管增减持数据.

    参考文档: https://www.lixinger.com/open/api/doc?api-key=cn/company/senior-executive-shares-change
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
        f"{settings.base_url}/cn/company/senior-executive-shares-change",
        json=payload,
    )
    df = get_response_df(response, Output)
    return df
