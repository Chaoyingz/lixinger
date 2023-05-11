from __future__ import annotations

import pandera as pa
import requests

from lixinger.config import settings
from lixinger.utils import api, get_response_df


class Output(pa.DataFrameModel):
    name: pa.typing.Series[str] = pa.Field(nullable=True)
    stock_code: pa.typing.Series[str]
    area_code: pa.typing.Series[str]
    market: pa.typing.Series[str]
    source: pa.typing.Series[str]
    currency: pa.typing.Series[str]
    series: pa.typing.Series[str]
    launch_date: pa.typing.Series[pa.typing.DateTime] = pa.Field(nullable=True)
    rebalancing_frequency: pa.typing.Series[str]
    caculation_method: pa.typing.Series[str]


@api
def get_index(
    stock_codes: list[str] | None = None,
) -> pa.typing.DataFrame[Output]:
    """获取指数详细信息.

    参考文档: https://www.lixinger.com/open/api/doc?api-key=cn/index
    """
    payload = {"token": settings.token, "stock_codes": stock_codes}

    response = requests.post(
        f"{settings.base_url}/cn/index",
        json=payload,
    )
    return get_response_df(response, Output)
