from __future__ import annotations

from typing import Literal, Optional

import pandas as pd
import pandera as pa
import requests
from pydantic import validate_arguments

from lixinger.config import settings
from lixinger.utils import convert_column_list_to_str, get_response_df


class Output(pa.DataFrameModel):
    name: pa.typing.Series[str] = pa.Field(nullable=True)
    stock_code: pa.typing.Series[str]
    area_code: pa.typing.Series[str]
    market: pa.typing.Series[str]
    fs_type: pa.typing.Series[str]
    mutual_markets: Optional[pa.typing.Series[str]] = pa.Field(nullable=True)
    ipo_date: pa.typing.Series[pa.typing.DateTime] = pa.Field(nullable=True)
    delisted_date: Optional[pa.typing.Series[pa.typing.DateTime]] = pa.Field(
        nullable=True
    )


@validate_arguments
@pa.check_types
def get_company(
    *,
    fs_type: Literal[
        "non_financial", "bank", "insurance", "security", "other_financial"
    ]
    | None = None,
    mutual_markets: Literal["ha"] | None = None,
    stock_codes: list[str] | None = None,
    include_delisted: bool | None = None,
) -> pa.typing.DataFrame[Output]:
    """获取股票详细信息.

    参考文档: https://www.lixinger.com/open/api/doc?api-key=cn/company
    """
    payload = {
        "token": settings.token,
    }
    if fs_type is not None:
        payload["fsType"] = fs_type
    if mutual_markets is not None:
        payload["mutualMarkets"] = mutual_markets
    if stock_codes is not None:
        payload["stockCodes"] = stock_codes
    if include_delisted is not None:
        payload["includeDelisted"] = include_delisted

    response = requests.post(
        f"{settings.base_url}/cn/company",
        json=payload,
    )
    df = get_response_df(response)
    df["ipo_date"] = pd.to_datetime(df["ipo_date"]).dt.tz_localize(None)
    if "delisted_date" in df.columns:
        df["delisted_date"] = pd.to_datetime(df["delisted_date"]).dt.tz_localize(None)

    if "mutual_markets" in df.columns:
        df["mutual_markets"] = [
            convert_column_list_to_str(column) for column in df["mutual_markets"]
        ]
    return df
