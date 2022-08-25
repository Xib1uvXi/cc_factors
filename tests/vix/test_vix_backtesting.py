from datetime import datetime
from factors.data.data import get_close_prices
from factors.vix.vix_backtesting import VixBacktesting


def test_vix_backtesting():
    symbol = "filusdt"
    interval = "1h"
    start_time = datetime(2021, 1, 1, 0, 0, 0)
    end_time = datetime(2022, 1, 1, 0, 0, 0)
    close = get_close_prices(symbol, interval, start_time, end_time)

    bt = VixBacktesting(close)
    bt.run()

    # print("raw capital: ", bt.raw_capital, "capital: ", bt.capital)
    # print("raw pos: ", bt.raw_pos, "pos: ", bt.pos)
    print("2021/1/1 - 2021/12/31 fil return", f"{100*((bt.pos - bt.raw_pos) / bt.raw_pos):,.2f}%")


def test_vix_backtesting_1():
    symbol = "filusdt"
    interval = "1h"
    start_time = datetime(2021, 1, 1, 0, 0, 0)
    end_time = datetime(2022, 8, 16, 0, 0, 0)
    close = get_close_prices(symbol, interval, start_time, end_time)

    bt = VixBacktesting(close)
    bt.run()

    # print("raw capital: ", bt.raw_capital, "capital: ", bt.capital)
    # print("raw pos: ", bt.raw_pos, "pos: ", bt.pos)
    print("2021/1/1 - 2022/8/16  fil return", f"{100*((bt.pos - bt.raw_pos) / bt.raw_pos):,.2f}%")


def test_vix_backtesting_2():
    symbol = "filusdt"
    interval = "1h"
    start_time = datetime(2021, 10, 1, 0, 0, 0)
    end_time = datetime(2022, 8, 16, 0, 0, 0)
    close = get_close_prices(symbol, interval, start_time, end_time)

    bt = VixBacktesting(close)
    bt.run()

    # print("raw capital: ", bt.raw_capital, "capital: ", bt.capital)
    # print("raw pos: ", bt.raw_pos, "pos: ", bt.pos)
    print("2021/10/1 - 2022/8/16  fil return", f"{100*((bt.pos - bt.raw_pos) / bt.raw_pos):,.2f}%")
