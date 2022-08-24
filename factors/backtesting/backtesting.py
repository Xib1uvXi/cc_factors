from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from enum import Enum
from datetime import date


class OrderDirection(Enum):
    BUY = 1
    SELL = 2


@dataclass
class Order:
    """Order is a dataclass that represents a single order.

    Attributes:
        quantity: The quantity of the order.
        price: The price of the order.
        timestamp: The timestamp of the order.
    """

    quantity: float
    price: float
    direction: OrderDirection


class Backtesting(ABC):
    def __init__(self, capital: float = 1000.0, pos: float = 0.0) -> None:
        self.trade_count: int = 0
        self.trades: List[Order] = []
        self.pending_order: Optional[Order] = None

        self.raw_capital = capital
        self.raw_pos = pos
        self.capital = capital
        self.pos = pos

    @abstractmethod
    def on_bar(self, close: float) -> None:
        pass

    def send_order(self, order: Order) -> None:
        if self.pending_order is None:
            self.pending_order = order
            return

        raise Exception("Pending order is not None")

    def next(self, close: float) -> None:
        # cross order
        self.cross_order()
        self.on_bar(close)
        pass

    def cross_order(self) -> None:
        order = self.pending_order
        if order is None:
            return

        if order.direction == OrderDirection.BUY:
            # check capital can buy order.quantity
            if self.capital < order.quantity * order.price:
                # FIXME: maybe can trade with some part of order.quantity
                self.pending_order = None
                return

            self.capital -= order.quantity * order.price
            self.pos += order.quantity

            self.trade_count += 1
            self.trades.append(order)

            self.pending_order = None
            return

        if order.direction == OrderDirection.SELL:
            # check pos can sell order.quantity
            if self.pos < order.quantity:
                # FIXME: maybe can trade with some part of order.quantity
                self.pending_order = None
                return

            self.capital += order.quantity * order.price
            self.pos -= order.quantity

            self.trade_count += 1
            self.trades.append(order)

            self.pending_order = None
            return

        return
