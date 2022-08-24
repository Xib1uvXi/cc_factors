from datetime import datetime
from factors.data.data import get_close_prices
from factors.vix.vix import Model
import pytest


def test_vix():
    symbol = "filusdt"
    interval = "1d"
    start_time = datetime(2020, 10, 16, 1, 1, 0)
    end_time = datetime(2022, 8, 16, 7, 59, 0)
    close = get_close_prices(symbol, interval, start_time, end_time)

    vix_model = Model(length=14).fit(close)
    vix_model.state.cu_up(1)


def test_vix_1h():
    symbol = "filusdt"
    interval = "1h"
    start_time = datetime(2020, 10, 16, 1, 1, 0)
    end_time = datetime(2022, 8, 16, 7, 59, 0)
    close = get_close_prices(symbol, interval, start_time, end_time)

    vix_model = Model(length=36).fit(close)
    df = vix_model.state.cu_up(24)

    # print(df[df["signal_cu_up"]])
