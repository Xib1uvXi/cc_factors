from dataclasses import dataclass
from typing import Optional

from typing_extensions import Self
import pandas as pd
import numpy as np
import pandas_ta as ta


@dataclass
class State:
    df: pd.DataFrame

    def cu_up(self, priod: int = 1) -> Optional[pd.DataFrame]:
        df = self.df.copy()

        df["diff_cu_up"] = df["vix"] - df["vix_ma_up"]
        df["signal_cu_up"] = (df["diff_cu_up"] < 0) & (df["diff_cu_up"].shift() >= 0)

        df["cu_up_priod_success"] = df["signal_cu_up"] & (df["close"].shift(-1 * priod) - df["close"] < 0)
        df["priod_diff_close"] = df["close"] - df["close"].shift(-1 * priod)

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
            df[["signal_cu_up", "cu_up_priod_success"]]
            .corr(method="spearman")
            .loc["signal_cu_up", "cu_up_priod_success"]
        )

        # calulate covariance
        cov = df[["signal_cu_up", "cu_up_priod_success"]].cov().loc["signal_cu_up", "cu_up_priod_success"]

        print("correlation", corr)
        print("covariance", cov)
        print("win_rate", win_rate)
        print("net_values", net_values[-1])

        return df


@dataclass
class Model:
    """Vix model"""

    length: int = 50
    state: Optional[State] = None

    def fit(self, close: pd.DataFrame) -> Self:
        # build indicator
        df = self.indicator(close)
        self.state = State(df)

        return self

    def indicator(self, df: pd.DataFrame) -> pd.DataFrame:
        vix = np.log(df["close"]) / np.log(df["close"].shift(self.length)) - 1
        vix_ma: pd.Series = ta.sma(vix, 20)

        assert vix_ma is not None

        # build indicator
        df["vix"] = vix
        df["vix_ma"] = vix_ma
        df["vix_ma_up"] = vix_ma.rolling(self.length, min_periods=0).max()
        df["vix_ma_down"] = vix_ma.rolling(self.length, min_periods=0).min()

        return df
