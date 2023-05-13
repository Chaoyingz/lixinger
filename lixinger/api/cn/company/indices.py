from __future__ import annotations

import pandera as pa

from lixinger import client
from lixinger.config import settings
from lixinger.utils import api, get_response_df


class Output(pa.DataFrameModel):
    area_code: pa.typing.Series[str]
    stock_code: pa.typing.Series[str]
    source: pa.typing.Series[str]


@api
def get_indices(
    stock_code: str,
    date: str | None = None,
) -> pa.typing.DataFrame[Output]:
    """获取股票所属指数信息.

    参考文档: https://www.lixinger.com/open/api/doc?api-key=cn/company/indices
    """
    payload = {
        "token": settings.token,
        "stockCode": stock_code,
    }
    if date is not None:
        payload["date"] = date

    response = client.post(
        f"{settings.base_url}/cn/company/indices",
        json=payload,
    )
    return get_response_df(response, Output)
