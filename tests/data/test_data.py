from datetime import datetime

import pandas_ta as ta  # pylint: disable=unused-import

from factors.data.data import get_close_prices
import numpy as np
import pandas as pd


def test_get_close_prices():
    symbol = "filusdt"
    interval = "1m"
    start_time = datetime(2021, 1, 1, 0, 0, 0)
    end_time = datetime(2021, 1, 1, 23, 59, 0)

    df = get_close_prices(symbol, interval, start_time, end_time)

    l = df.to_dict("records")

    assert len(l) == 1440


def test_vix_model():
    symbol = "filusdt"
    interval = "1m"
    start_time = datetime(2021, 1, 1, 0, 0, 0)
    end_time = datetime(2021, 1, 1, 0, 59, 0)

    df = get_close_prices(symbol, interval, start_time, end_time)

    l = df.to_dict("records")
    assert len(l) == 60

    vix = np.log(df["close"]) / np.log(df["close"].shift(20)) - 1
    # print(vix)

    vix_ma: pd.Series = ta.sma(vix, 20)

    # vix_ma_up = ta.m

    df["vix"] = vix
    df["vix_ma"] = vix_ma
    df["vix_ma_up"] = vix_ma.rolling(20, min_periods=0).max()
    df["vix_ma_down"] = vix_ma.rolling(20, min_periods=0).min()

    df["x"] = df["vix"] - df["vix_ma_down"]

    # print(df)
    x = df["x"]
    shorts = (x < 0) & (x.shift() >= 0)
    y = df.loc[shorts]
    # print(y)

    # vix = np.log(df["close"].sort_index(ascending=False)) / np.log(df["close"].shift)
