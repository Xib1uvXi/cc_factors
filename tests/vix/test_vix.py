from datetime import datetime
from factors.data.data import get_close_prices
from factors.vix.vix import Model
import pandas as pd


def vix_indicators(df: pd.DataFrame, msg: str = "") -> None:
    # Indicators
    # win rate
    win_rate = df["cu_up_priod_success"].sum() / df["signal_cu_up"].sum()

    # net_values
    signal_close = df[df["signal_cu_up"]]["close"]
    signal_priod_diff_close = df[df["signal_cu_up"]]["priod_diff_close"]
    amplitudes = signal_priod_diff_close / signal_close
    net_values = (1 + amplitudes).cumprod()

    # calculate correlation
    corr = (
        df[["signal_cu_up", "cu_up_priod_success"]].corr(method="spearman").loc["signal_cu_up", "cu_up_priod_success"]
    )

    # calulate covariance
    cov = df[["signal_cu_up", "cu_up_priod_success"]].cov().loc["signal_cu_up", "cu_up_priod_success"]

    print("=================", msg, "=================")
    print("correlation", corr)
    print("covariance", cov)
    print("win_rate", win_rate)
    print("net_values", net_values[-1])


def test_vix():
    symbol = "filusdt"
    interval = "1d"
    start_time = datetime(2020, 10, 16, 1, 1, 0)
    end_time = datetime(2022, 8, 16, 7, 59, 0)
    close = get_close_prices(symbol, interval, start_time, end_time)

    vix_model = Model(length=14).fit(close)

    vix_indicators(vix_model.state.cu_up(1), "filusdt-1d")


def test_vix_1h():
    symbol = "filusdt"
    interval = "1h"
    start_time = datetime(2020, 10, 16, 1, 1, 0)
    end_time = datetime(2022, 8, 16, 7, 59, 0)
    close = get_close_prices(symbol, interval, start_time, end_time)

    vix_model = Model(length=36).fit(close)

    vix_indicators(vix_model.state.cu_up(24), "filusdt-1h")


def test_vix_1h_vsbao():
    symbol = "filusdt"
    interval = "1h"
    start_time = datetime(2021, 10, 1, 0, 0, 0)
    end_time = datetime(2022, 8, 16, 8, 0, 0)
    close = get_close_prices(symbol, interval, start_time, end_time)

    vix_model = Model(length=36).fit(close)

    vix_indicators(vix_model.state.cu_up(24), "filusdt-1h_vs_bao")
