from __future__ import annotations

import pandas as pd
import pandera as pa

from lixinger import client
from lixinger.config import settings
from lixinger.utils import api, get_response_df, set_column_snake_case


class Output(pa.DataFrameModel):
    index_code: pa.typing.Series[str]
    stock_code: pa.typing.Series[str]
    aera_code: pa.typing.Series[str]
    market: pa.typing.Series[str]


@api
def get_index_constituents(
    date: str,
    stock_codes: list[str] = None,
) -> pa.typing.DataFrame[Output]:
    """获取样本信息.

    参考文档: https://www.lixinger.com/open/api/doc?api-key=cn/index/constituents
    """
    payload = {
        "token": settings.token,
        "date": date,
    }
    if stock_codes is not None:
        payload["stockCodes"] = stock_codes
    response = client.post(
        f"{settings.base_url}/cn/index/constituents",
        json=payload,
    )
    df = get_response_df(response, Output)
    del df["index_code"]
    del df["market"]
    del df["aera_code"]
    df = df.explode("constituents")
    df = pd.concat(
        [df.drop(["constituents"], axis=1), df["constituents"].apply(pd.Series)], axis=1
    )
    df.rename(columns={"stock_code": "index_code"}, inplace=True)
    df = set_column_snake_case(df)
    return df
