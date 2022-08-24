from datetime import datetime
from factors.data.data import get_close_prices
from factors.vix.vix import Model


def test_vix():
    symbol = "filusdt"
    interval = "1d"
    start_time = datetime(2020, 10, 16, 1, 1, 0)
    end_time = datetime(2022, 8, 16, 7, 59, 0)
    close = get_close_prices(symbol, interval, start_time, end_time)

    vix_model = Model(length=5).fit(close)
    vix_model.state.cu_up(2)
