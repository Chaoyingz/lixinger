import requests
from requests import Response, request
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    stop_after_delay,
    wait_fixed,
)


@retry(
    stop=(stop_after_delay(60) | stop_after_attempt(3)),
    wait=wait_fixed(3),
    retry=retry_if_exception_type(
        (requests.exceptions.Timeout, requests.exceptions.ProxyError)
    ),
)
def post(url: str, data=None, json=None, **kwargs: any) -> Response:
    return request("post", url, data=data, json=json, **kwargs)
