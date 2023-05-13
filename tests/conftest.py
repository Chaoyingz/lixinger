import time

import pytest


@pytest.fixture(autouse=True)
def slow_down_tests():
    yield
    time.sleep(0.5)
