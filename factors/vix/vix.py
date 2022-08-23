from dataclasses import dataclass
from typing import Optional

from typing_extensions import Self
import pandas as pd
import numpy as np
import pandas_ta as ta


@dataclass
class State:
    corr: float
    df: pd.DataFrame


@dataclass
class Model:
    """Vix model"""

    length: int = 50
    state: Optional[State] = None

    def fit(self, close: pd.DataFrame) -> Self:
        df = self.indicator(close)

        # calculate correlation
        corr = df[["close", "vix_ma"]].corr(method="spearman").loc["close", "vix_ma"]

        self.state = State(corr, df)

        return self

    def indicator(self, df: pd.DataFrame) -> pd.DataFrame:
        vix = np.log(df["close"]) / np.log(df["close"].shift(self.length - 1)) - 1
        vix_ma: pd.Series = ta.sma(vix, 20)

        # build indicator
        df["vix"] = vix
        df["vix_ma"] = vix_ma
        df["vix_ma_up"] = vix_ma.rolling(self.length, min_periods=0).max()
        df["vix_ma_down"] = vix_ma.rolling(self.length, min_periods=0).min()

        # FIXME: this is not working
        df["diff"] = df["vix"] - df["vix_ma_up"]
        df["signal"] = (df["diff"] < 0) & (df["diff"].shift() >= 0)

        return df
