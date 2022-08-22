import os.path
from datetime import datetime
from typing import Optional

import myloginpath
import pandas as pd
from pyarrow import feather

conf = myloginpath.parse("client")
conn = f"mysql://{conf['user']}:{conf['password']}@{conf['host']}/binance_data"


def get_close_prices(
    symbol: str, interval: str, start: Optional[datetime] = None, end: Optional[datetime] = None
) -> pd.DataFrame:
    """获取收盘价格

    Args:
        symbol (str): 标的名称
        interval (str): 周期级别
        start (Optional[datetime], optional): 开始时间. Defaults to None.
        end (Optional[datetime], optional): 结束时间. Defaults to None.

    Returns:
        pd.DataFrame: 收盘价时间序列
    """

    filename = f"tmp/prices_{symbol}_{interval}_{start}_{end}.feather"
    if os.path.exists(filename):
        return feather.read_feather(filename)

    sql = "select b.datetime as updated_at, b.close_price price" f" from bars_{symbol}_{interval} b where 1=1"

    if start:
        sql += f" and b.datetime >= '{start}'"

    if end:
        sql += f" and b.datetime <= '{end}'"

    sql += " order by b.datetime asc"
    df = pd.read_sql(sql, conn).set_index("updated_at")

    feather.write_feather(df, filename)
    return df
