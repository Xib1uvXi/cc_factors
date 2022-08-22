"""correlation.py - 生成相关系数矩阵
"""
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots


def show(df: pd.DataFrame) -> None:
    """生成相关系数矩阵

    Args:
        df (pd.DataFrame): Price-Balance 数据
    """
    fig = make_subplots(
        rows=1,
        cols=3,
        subplot_titles=(
            "皮尔逊积矩相关系数 (Pearson correlation coefficient)",
            "肯德尔等级相关系数 (Kendall rank correlation coefficient)",
            "斯皮尔曼等级相关系数 (Spearman's rank correlation coefficient)",
        ),
    )

    def generate_heatmap(df: pd.DataFrame, col: int):
        fig.add_trace(
            go.Heatmap(
                x=df.columns,
                y=df.index,
                z=np.array(df),
                text=df.values,
                texttemplate="%{text:.2f}",
                colorscale=px.colors.diverging.RdBu,
            ),
            row=1,
            col=col,
        )

    generate_heatmap(df.corr(method="pearson"), 1)
    generate_heatmap(df.corr(method="kendall"), 2)
    generate_heatmap(df.corr(method="spearman"), 3)

    fig.update_layout(
        title="相关系数矩阵 (Correlation matrix)",
        font=dict(family="Courier New, monospace", size=18, color="RebeccaPurple"),
    )

    fig.show()
