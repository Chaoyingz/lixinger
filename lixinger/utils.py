from __future__ import annotations

import re
from functools import wraps
from typing import Type

import numpy as np
import pandas as pd
import pandera as pa
from requests import Response


def camel_case_to_snake_case(name: str) -> str:
    """Convert camel case to snake case."""
    pattern = re.compile(r"(?<!^)(?=[A-Z])")
    name = pattern.sub("_", name).lower()
    return name


def set_column_snake_case(df: pd.DataFrame) -> pd.DataFrame:
    """Set dataframe column names to snake case."""
    df.columns = [camel_case_to_snake_case(col) for col in df.columns]
    return df


def convert_column_list_to_str(column: list[str]) -> str:
    """Convert column list to string."""
    try:
        return ",".join(map(str, column))
    except TypeError:
        return np.NaN


def get_response_data(response: Response) -> list[dict[str, any]]:
    """Get response data from response."""
    resp_json = response.json()
    if resp_json.get("code") != 1:
        raise ValueError(f"[{resp_json.get('code')}]{resp_json.get('error')}")
    return resp_json["data"]


def get_response_df(
    response: Response, output: Type[pa.DataFrameModel]
) -> pd.DataFrame:
    """Get response dataframe from response."""
    data = get_response_data(response)
    dtypes = {k: str(v) for k, v in output.to_schema().dtypes.items()}
    if not data:
        df = pd.DataFrame(columns=[*dtypes]).astype(dtypes)
    else:
        df = pd.json_normalize(data)
        df = set_column_snake_case(df)
        missing_columns = set(dtypes.keys()) - set(df.columns)
        if missing_columns:
            df[list(missing_columns)] = np.NaN
        df = df.astype(dtypes, errors="ignore")
        for col, dtype in dtypes.items():
            if dtype == "datetime64[ns]":
                df[col] = pd.to_datetime(df[col]).dt.tz_localize(None)
    return df


def adjust_request_date_range(func: callable) -> callable:
    """Adjust request date range."""

    @wraps(func)
    def wrapper(*args: any, **kwargs: any) -> callable:
        start_date_str = kwargs.get("start_date")
        end_date_str = kwargs.get("end_date")
        limit = kwargs.get("limit")

        if start_date_str is None:
            raise ValueError("start_date is required")
        start_date = pd.Timestamp(start_date_str)

        if end_date_str is None:
            end_date = pd.Timestamp("today")
        else:
            end_date = pd.Timestamp(end_date_str)

        if start_date > end_date:
            raise ValueError("start_date should be less than end_date")

        dfs = pd.DataFrame()
        while start_date < end_date:
            new_end_date = start_date + pd.DateOffset(years=10)
            query_params = {
                **kwargs,
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": new_end_date.strftime("%Y-%m-%d"),
            }
            df = func(*args, **query_params)
            dfs = pd.concat([dfs, df])
            start_date = new_end_date + pd.Timedelta(days=1)

            if limit is not None:
                limit -= len(df)
                if limit <= 0:
                    break
                kwargs["limit"] = limit
        if "date" in dfs.columns:
            dfs.sort_values(by="date", inplace=True)
        return dfs

    return wrapper
