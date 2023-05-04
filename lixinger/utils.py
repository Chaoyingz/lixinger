from __future__ import annotations

import re

import numpy as np
import pandas as pd
from requests import Response


def camel_case_to_snake_case(name: str) -> str:
    pattern = re.compile(r"(?<!^)(?=[A-Z])")
    name = pattern.sub("_", name).lower()
    return name


def set_column_snake_case(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [camel_case_to_snake_case(col) for col in df.columns]
    return df


def convert_column_list_to_str(column):
    try:
        return ",".join(map(str, column))
    except TypeError:
        return np.nan


def get_response_data(response: Response) -> list[dict[str, any]]:
    resp_json = response.json()
    if resp_json.get("code") != 1:
        raise ValueError(f"[{resp_json.get('code')}]{resp_json.get('error')}")
    return resp_json["data"]


def get_response_df(response: Response) -> pd.DataFrame:
    data = get_response_data(response)
    df = pd.json_normalize(data)
    df = set_column_snake_case(df)
    return df
