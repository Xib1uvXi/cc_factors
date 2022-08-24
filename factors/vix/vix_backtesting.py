from optparse import Option
from typing import Optional
from factors.backtesting.backtesting import Backtesting, Order, OrderDirection
from factors.vix.vix import Model
import pandas as pd


class VixBacktesting(Backtesting):
    model: Model

    vix0: Optional[float] = None
    vix1: Optional[float] = None
    vix_ma_up0: Optional[float] = None
    vix_ma_up1: Optional[float] = None

    latest_close: float

    def __init__(self, data: pd.DataFrame, size: float = 10, capital: float = 0, pos: float = 100) -> None:
        super().__init__(capital, pos)
        self.model = Model().fit(data)
        self.size = size
        self.buy_count: Optional[int] = None

    def on_bar(self, close: float) -> None:
        if not (
            self.vix0 is not None
            and self.vix1 is not None
            and self.vix_ma_up0 is not None
            and self.vix_ma_up1 is not None
        ):
            return

        if self.buy_count is not None:
            if self.buy_count == 24:
                self.buy_count = None
                self.send_order(Order(quantity=(self.capital / close), price=close, direction=OrderDirection.BUY))
                return

        if self.vix0 < self.vix_ma_up0 and self.vix1 >= self.vix_ma_up1:
            if self.pos >= self.size:
                self.send_order(Order(quantity=self.pos, price=close, direction=OrderDirection.SELL))
                self.buy_count = 1
                return

        if self.buy_count is not None:
            self.buy_count += 1

    def run(self) -> None:
        for i in range(len(self.model.state.df)):

            vix = self.model.state.df.iloc[i]["vix"]
            vix_ma = self.model.state.df.iloc[i]["vix_ma"]

            self.vix1 = self.vix0
            self.vix0 = vix

            self.vix_ma_up1 = self.vix_ma_up0
            self.vix_ma_up0 = vix_ma

            close = self.model.state.df.iloc[i]["close"]

            self.latest_close = close
            self.next(close)

        if self.capital > 0:
            self.pos += self.capital / self.latest_close
            self.capital = 0
