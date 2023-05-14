from __future__ import annotations

from typing import Literal

import pandera as pa

from lixinger import client
from lixinger.config import settings
from lixinger.utils import api, get_response_df


class Output(pa.DataFrameModel):
    date: pa.typing.Series[pa.typing.DateTime]
    stock_code: pa.typing.Series[str]


@api
def get_fundamental_statistics(
    stock_codes: list[str],
    metrics_list: list[str],
    granularity: Literal["y10", "y5", "y3"],
) -> pa.typing.DataFrame[Output]:
    """获取基本面统计数据.

    参考文档: https://www.lixinger.com/open/api/doc?api-key=cn/company/fundamental-statistics
    """
    payload = {
        "token": settings.token,
        "stockCodes": stock_codes,
        "metricsList": metrics_list,
        "granularity": granularity,
    }

    response = client.post(
        f"{settings.base_url}/cn/company/fundamental-statistics",
        json=payload,
    )
    return get_response_df(response, Output)
