from datetime import datetime

import pandas_ta as ta  # pylint: disable=unused-import

from factors.data.data import get_close_prices


def test_get_close_prices():
    symbol = "filusdt"
    interval = "1m"
    start_time = datetime(2021, 1, 1, 0, 0, 0)
    end_time = datetime(2021, 1, 1, 23, 59, 0)

    df = get_close_prices(symbol, interval, start_time, end_time)

    l = df.to_dict("records")

    assert len(l) == 1440

    # print(df.ta.sma(length=10))
