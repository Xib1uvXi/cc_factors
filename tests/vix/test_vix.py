from datetime import datetime
from factors.data.data import get_close_prices
from factors.vix.vix import Model


def test_vix():
    symbol = "filusdt"
    interval = "1d"
    start_time = datetime(2021, 1, 1, 0, 0, 0)
    end_time = datetime(2021, 12, 1, 23, 59, 0)
    close = get_close_prices(symbol, interval, start_time, end_time)

    vix_model = Model(length=36).fit(close)

    # print(vix_model.state.corr)
    # print(vix_model.state.df)

    df = vix_model.state.df

    priod = 1
    df["success"] = (df["close"] < df["close"].shift(priod)) & df["signal"].shift(priod) == 1

    print(df["success"].sum() / df["signal"].sum() * 100)

    print(df[df["signal"]])
