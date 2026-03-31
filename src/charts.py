"""Reusable Plotly chart builders for the trading dashboard."""

from typing import Dict, List

import plotly.graph_objects as go

_BG = "#0d1520"
_BG2 = "#1a2332"
_GRID = "#2a3a4a"
_TEXT = "#e8eef4"
_TEXT2 = "#90b0c8"
_POSITIVE = "#4caf7d"
_NEGATIVE = "#e05050"
_NEUTRAL = "#7098b0"
_ACCENT = "#6cc0e0"
_ZERO = "#4a5a6a"


def _base_layout(**kwargs) -> dict:
    base = dict(
        plot_bgcolor=_BG2,
        paper_bgcolor=_BG,
        font=dict(color=_TEXT, size=12),
        margin=dict(l=20, r=30, t=40, b=30),
    )
    base.update(kwargs)
    return base


def indicator_bar_chart(signal: Dict, title: str = "") -> go.Figure:
    """Horizontal bar chart showing all indicator scores for one pair.

    Displays individual indicators, composite technical score,
    sentiment score, and fused signal — all on the same -1 to +1 scale.
    """
    labels = [
        "EMA Crossover",
        "RSI",
        "MACD",
        "Bollinger Bands",
        "",  # spacer
        "Technical (composite)",
        "Sentiment (FinBERT)",
        "",  # spacer
        "Final Signal",
    ]
    values = [
        signal["indicators"]["ema_crossover"],
        signal["indicators"]["rsi"],
        signal["indicators"]["macd"],
        signal["indicators"]["bollinger"],
        None,
        signal["technical_score"],
        signal["sentiment_score"],
        None,
        signal["signal"],
    ]

    bar_labels = [l for l, v in zip(labels, values) if v is not None]
    bar_values = [v for v in values if v is not None]
    bar_colors = []
    for i, v in enumerate(bar_values):
        if i == len(bar_values) - 1:
            bar_colors.append(_ACCENT)
        elif v >= 0:
            bar_colors.append(_POSITIVE)
        else:
            bar_colors.append(_NEGATIVE)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=bar_values,
        y=bar_labels,
        orientation="h",
        marker_color=bar_colors,
        marker_line_width=0,
        text=[f"{v:+.3f}" for v in bar_values],
        textposition="outside",
        textfont=dict(size=11, color=_TEXT2),
        cliponaxis=False,
    ))

    fig.update_layout(
        **_base_layout(height=320, title=dict(text=title, font=dict(size=13, color=_TEXT2))),
        xaxis=dict(
            range=[-1.35, 1.35],
            zeroline=True,
            zerolinecolor=_ZERO,
            zerolinewidth=2,
            gridcolor=_GRID,
            tickvals=[-1, -0.5, 0, 0.5, 1],
            ticktext=["−1", "−0.5", "0", "+0.5", "+1"],
        ),
        yaxis=dict(automargin=True, gridcolor="rgba(0,0,0,0)"),
        shapes=[
            dict(type="line", x0=-0.5, x1=-0.5, y0=-0.5, y1=len(bar_labels) - 0.5,
                 line=dict(color=_NEUTRAL, width=1, dash="dot")),
            dict(type="line", x0=0.5, x1=0.5, y0=-0.5, y1=len(bar_labels) - 0.5,
                 line=dict(color=_NEUTRAL, width=1, dash="dot")),
        ],
        showlegend=False,
    )
    return fig


def equity_curve_chart(equity: List[float], title: str = "Equity Curve") -> go.Figure:
    """Line chart of equity curve with fill."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=equity,
        mode="lines",
        line=dict(color=_ACCENT, width=2),
        fill="tozeroy",
        fillcolor="rgba(108,192,224,0.08)",
        name="Equity",
        hovertemplate="Candle %{x}<br>$%{y:,.2f}<extra></extra>",
    ))
    fig.update_layout(
        **_base_layout(height=320, title=dict(text=title, font=dict(size=13, color=_TEXT2))),
        xaxis=dict(title="Candle", gridcolor=_GRID),
        yaxis=dict(title="Portfolio Value ($)", gridcolor=_GRID, tickformat="$,.0f"),
        showlegend=False,
    )
    return fig


def equity_with_drawdown(equity: List[float]) -> go.Figure:
    """Two-panel figure: equity curve on top, drawdown on bottom."""
    import numpy as np
    eq = [float(e) for e in equity]
    peak = [max(eq[:i+1]) for i in range(len(eq))]
    drawdown = [(e - p) / p * 100 for e, p in zip(eq, peak)]

    from plotly.subplots import make_subplots
    fig = make_subplots(rows=2, cols=1, row_heights=[0.65, 0.35], vertical_spacing=0.06)

    fig.add_trace(go.Scatter(
        y=eq, mode="lines",
        line=dict(color=_ACCENT, width=2),
        fill="tozeroy", fillcolor="rgba(108,192,224,0.08)",
        name="Equity",
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        y=drawdown, mode="lines",
        line=dict(color=_NEGATIVE, width=1.5),
        fill="tozeroy", fillcolor="rgba(224,80,80,0.15)",
        name="Drawdown %",
    ), row=2, col=1)

    fig.update_layout(
        **_base_layout(height=440),
        showlegend=False,
    )
    fig.update_yaxes(gridcolor=_GRID, title_text="Value ($)", tickformat="$,.0f", row=1, col=1)
    fig.update_yaxes(gridcolor=_GRID, title_text="Drawdown %", ticksuffix="%", row=2, col=1)
    fig.update_xaxes(gridcolor=_GRID, title_text="Candle", row=2, col=1)
    fig.update_xaxes(gridcolor=_GRID, showticklabels=False, row=1, col=1)
    return fig


def pnl_histogram(trades: List[Dict]) -> go.Figure:
    """Histogram of trade P&L percentages."""
    pnls = [t["pnl_pct"] * 100 for t in trades]
    colors = [_POSITIVE if p > 0 else _NEGATIVE for p in pnls]

    fig = go.Figure(go.Histogram(
        x=pnls,
        nbinsx=20,
        marker_color=_ACCENT,
        marker_line_color=_BG,
        marker_line_width=0.5,
        opacity=0.85,
        name="P&L %",
        hovertemplate="%{x:.2f}%<extra></extra>",
    ))
    fig.add_vline(x=0, line_color=_ZERO, line_width=2)
    fig.update_layout(
        **_base_layout(height=280, title=dict(text="Trade P&L Distribution", font=dict(size=13, color=_TEXT2))),
        xaxis=dict(title="P&L %", gridcolor=_GRID, ticksuffix="%"),
        yaxis=dict(title="Count", gridcolor=_GRID),
        showlegend=False,
    )
    return fig
