from __future__ import annotations

import pandera as pa
import requests
from pydantic import validate_arguments

from lixinger.config import settings
from lixinger.utils import get_response_df


class Output(pa.DataFrameModel):
    area_code: pa.typing.Series[str]
    stock_code: pa.typing.Series[str]
    source: pa.typing.Series[str]


@validate_arguments
@pa.check_types
def get_industries(
    stock_code: str,
    date: str | None = None,
) -> pa.typing.DataFrame[Output]:
    """获取股票所属行业信息.

    参考文档: https://www.lixinger.com/open/api/doc?api-key=cn/company/industries
    """
    payload = {
        "token": settings.token,
        "stockCode": stock_code,
    }
    if date is not None:
        payload["date"] = date

    response = requests.post(
        f"{settings.base_url}/cn/company/industries",
        json=payload,
    )
    return get_response_df(response, Output)
