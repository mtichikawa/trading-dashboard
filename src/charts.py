"""Reusable Plotly chart builders for the trading dashboard."""

import statistics
from typing import Dict, List

import plotly.graph_objects as go
from plotly.subplots import make_subplots

_BG = "#0d1520"
_BG2 = "#1a2332"
_GRID = "#2a3a4a"
_TEXT = "#e8eef4"
_TEXT2 = "#90b0c8"
_POSITIVE = "#4caf7d"
_NEGATIVE = "#e05050"
_NEUTRAL = "#7098b0"
_ACCENT = "#6cc0e0"
_ACCENT2 = "#9b7fe8"   # purple — composite scores
_ZERO = "#4a5a6a"

_CHART_CONFIG = {
    "displayModeBar": "hover",
    "displaylogo": False,
    "doubleClick": "reset+autosize",
    "modeBarButtonsToRemove": ["lasso2d", "select2d"],
}


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

    Three color-coded groups: individual indicators (blue), composite
    scores (purple), final fused signal (accent/white).
    """
    fig = go.Figure()

    # --- Group 1: individual technical indicators ---
    ind = signal["indicators"]
    ind_labels = ["EMA Crossover", "RSI", "MACD", "Bollinger Bands"]
    ind_values = [ind["ema_crossover"], ind["rsi"], ind["macd"], ind["bollinger"]]
    fig.add_trace(go.Bar(
        x=ind_values,
        y=ind_labels,
        orientation="h",
        name="Indicators",
        marker_color=[_ACCENT if v >= 0 else "#3a7a9a" for v in ind_values],
        marker_line_width=0,
        opacity=0.85,
        text=[f"{v:+.3f}" for v in ind_values],
        textposition="outside",
        textfont=dict(size=11, color=_TEXT2),
        cliponaxis=False,
        hovertemplate="%{y}: %{x:+.3f}<extra></extra>",
    ))

    # --- Group 2: composite scores ---
    comp_labels = ["Technical (composite)", "Sentiment (FinBERT)"]
    comp_values = [signal["technical_score"], signal["sentiment_score"]]
    fig.add_trace(go.Bar(
        x=comp_values,
        y=comp_labels,
        orientation="h",
        name="Composite",
        marker_color=[_ACCENT2 if v >= 0 else "#6040a0" for v in comp_values],
        marker_line_width=0,
        opacity=0.9,
        text=[f"{v:+.3f}" for v in comp_values],
        textposition="outside",
        textfont=dict(size=11, color=_TEXT2),
        cliponaxis=False,
        hovertemplate="%{y}: %{x:+.3f}<extra></extra>",
    ))

    # --- Group 3: final fused signal ---
    sig_val = signal["signal"]
    fig.add_trace(go.Bar(
        x=[sig_val],
        y=["Final Signal"],
        orientation="h",
        name="Signal",
        marker_color=_POSITIVE if sig_val >= 0 else _NEGATIVE,
        marker_line_color=_TEXT,
        marker_line_width=1,
        text=[f"{sig_val:+.3f}"],
        textposition="outside",
        textfont=dict(size=12, color=_TEXT),
        cliponaxis=False,
        hovertemplate="Signal: %{x:+.3f}<extra></extra>",
    ))

    # Divider lines between sections
    all_labels = ind_labels + comp_labels + ["Final Signal"]
    n_ind = len(ind_labels)
    n_comp = len(comp_labels)

    fig.update_layout(
        **_base_layout(
            height=360,
            title=dict(text=title, font=dict(size=13, color=_TEXT2)),
        ),
        xaxis=dict(
            range=[-1.45, 1.45],
            zeroline=True,
            zerolinecolor=_ZERO,
            zerolinewidth=2,
            gridcolor=_GRID,
            tickvals=[-1, -0.5, 0, 0.5, 1],
            ticktext=["−1", "−0.5", "0", "+0.5", "+1"],
        ),
        yaxis=dict(
            automargin=True,
            gridcolor="rgba(0,0,0,0)",
            categoryorder="array",
            categoryarray=all_labels[::-1],
        ),
        shapes=[
            # threshold reference zones
            dict(type="rect", x0=-0.5, x1=0.5, y0=-0.5, y1=len(all_labels) - 0.5,
                 fillcolor="rgba(108,192,224,0.04)", line_width=0, layer="below"),
            # section dividers
            dict(type="line", x0=-1.4, x1=1.4,
                 y0=n_ind - 0.5, y1=n_ind - 0.5,
                 line=dict(color=_GRID, width=1, dash="dot")),
            dict(type="line", x0=-1.4, x1=1.4,
                 y0=n_ind + n_comp - 0.5, y1=n_ind + n_comp - 0.5,
                 line=dict(color=_GRID, width=1.5, dash="dot")),
        ],
        annotations=[
            dict(text="INDICATORS", x=-1.43, y=n_ind - 0.5 + 0.1,
                 xanchor="left", yanchor="bottom",
                 font=dict(size=9, color=_ZERO), showarrow=False),
            dict(text="COMPOSITE", x=-1.43, y=n_ind + n_comp - 0.5 + 0.1,
                 xanchor="left", yanchor="bottom",
                 font=dict(size=9, color=_ZERO), showarrow=False),
            dict(text="SIGNAL", x=-1.43, y=len(all_labels) - 0.5 + 0.1,
                 xanchor="left", yanchor="bottom",
                 font=dict(size=9, color=_ZERO), showarrow=False),
        ],
        showlegend=False,
        barmode="overlay",
    )
    return fig


def equity_curve_chart(equity: List[float], title: str = "Equity Curve") -> go.Figure:
    """Equity curve with conditional green/red fill relative to starting value."""
    start = equity[0]
    x = list(range(len(equity)))
    current = equity[-1]
    total_return = (current - start) / start * 100
    color = _POSITIVE if current >= start else _NEGATIVE

    fig = go.Figure()

    # Reference line at starting equity
    fig.add_hline(
        y=start,
        line_color=_ZERO,
        line_width=1.5,
        line_dash="dash",
        annotation_text=f"Start ${start:,.0f}",
        annotation_position="bottom right",
        annotation_font=dict(size=10, color=_ZERO),
    )

    # Fill below the curve — conditional color
    fig.add_trace(go.Scatter(
        x=x, y=equity,
        mode="lines",
        line=dict(color=color, width=2.5),
        fill="tonexty",
        fillcolor=f"rgba({'76,175,125' if current >= start else '224,80,80'},0.15)",
        name="Equity",
        hovertemplate="Candle %{x}<br><b>$%{y:,.2f}</b><extra></extra>",
    ))

    # Annotation for current value
    fig.add_annotation(
        x=len(equity) - 1,
        y=current,
        text=f"${current:,.0f}<br><span style='font-size:10px'>{total_return:+.2f}%</span>",
        showarrow=True,
        arrowhead=0,
        arrowcolor=color,
        arrowwidth=1.5,
        ax=40,
        ay=0,
        font=dict(size=11, color=color),
        bgcolor=_BG2,
        bordercolor=color,
        borderwidth=1,
        borderpad=4,
    )

    fig.update_layout(
        **_base_layout(
            height=340,
            title=dict(text=title, font=dict(size=13, color=_TEXT2)),
        ),
        xaxis=dict(title="Candle", gridcolor=_GRID, showgrid=True),
        yaxis=dict(title="Portfolio Value ($)", gridcolor=_GRID, tickformat="$,.0f"),
        showlegend=False,
    )
    return fig


def equity_with_drawdown(equity: List[float]) -> go.Figure:
    """Two-panel figure: equity curve on top, drawdown % on bottom.

    Drawdown panel has shaded severity zones at -5%, -10%, -20%.
    """
    eq = [float(e) for e in equity]
    n = len(eq)
    peak = []
    running_max = eq[0]
    for e in eq:
        running_max = max(running_max, e)
        peak.append(running_max)
    drawdown = [(e - p) / p * 100 for e, p in zip(eq, peak)]

    max_dd = min(drawdown)
    max_dd_idx = drawdown.index(max_dd)
    start = eq[0]
    current = eq[-1]
    total_return = (current - start) / start * 100
    eq_color = _POSITIVE if current >= start else _NEGATIVE

    fig = make_subplots(
        rows=2, cols=1,
        row_heights=[0.65, 0.35],
        vertical_spacing=0.04,
        shared_xaxes=True,
    )

    # --- Equity panel ---
    fig.add_hline(y=start, line_color=_ZERO, line_width=1, line_dash="dash", row=1, col=1)

    fig.add_trace(go.Scatter(
        x=list(range(n)), y=eq,
        mode="lines",
        line=dict(color=eq_color, width=2.5),
        fill="tozeroy",
        fillcolor=f"rgba({'76,175,125' if current >= start else '224,80,80'},0.12)",
        name="Equity",
        hovertemplate="Candle %{x}<br><b>$%{y:,.2f}</b><extra></extra>",
    ), row=1, col=1)

    # Peak annotation
    peak_idx = eq.index(max(eq))
    fig.add_annotation(
        x=peak_idx, y=max(eq),
        text=f"Peak ${max(eq):,.0f}",
        showarrow=True, arrowhead=2, arrowcolor=_TEXT2, arrowwidth=1,
        ax=0, ay=-28,
        font=dict(size=10, color=_TEXT2),
        row=1, col=1,
    )

    # Current value annotation
    fig.add_annotation(
        x=n - 1, y=current,
        text=f"${current:,.0f} ({total_return:+.2f}%)",
        showarrow=True, arrowhead=0, arrowcolor=eq_color, arrowwidth=1.5,
        ax=50, ay=0,
        font=dict(size=10, color=eq_color),
        bgcolor=_BG2, bordercolor=eq_color, borderwidth=1, borderpad=3,
        row=1, col=1,
    )

    # --- Drawdown panel ---
    # Severity zone shading
    zones = [
        (-5,  0,   "rgba(224,200,80,0.06)"),   # mild
        (-10, -5,  "rgba(224,140,50,0.08)"),   # moderate
        (-20, -10, "rgba(224,80,80,0.10)"),    # severe
        (-50, -20, "rgba(180,50,50,0.12)"),    # extreme
    ]
    for y0, y1, color in zones:
        fig.add_hrect(y0=y0, y1=y1, fillcolor=color, line_width=0, row=2, col=1)

    # Reference lines at severity thresholds
    for level, label in [(-5, "-5%"), (-10, "-10%"), (-20, "-20%")]:
        fig.add_hline(
            y=level, line_color=_ZERO, line_width=1, line_dash="dot",
            annotation_text=label, annotation_position="right",
            annotation_font=dict(size=9, color=_ZERO),
            row=2, col=1,
        )

    fig.add_trace(go.Scatter(
        x=list(range(n)), y=drawdown,
        mode="lines",
        line=dict(color=_NEGATIVE, width=2),
        fill="tozeroy",
        fillcolor="rgba(224,80,80,0.25)",
        name="Drawdown",
        hovertemplate="Candle %{x}<br>Drawdown: %{y:.2f}%<extra></extra>",
    ), row=2, col=1)

    # Max drawdown annotation
    fig.add_annotation(
        x=max_dd_idx, y=max_dd,
        text=f"Max DD<br>{max_dd:.1f}%",
        showarrow=True, arrowhead=2, arrowcolor=_NEGATIVE, arrowwidth=1.5,
        ax=0, ay=25,
        font=dict(size=10, color=_NEGATIVE),
        row=2, col=1,
    )

    fig.update_layout(
        **_base_layout(height=480),
        showlegend=False,
    )
    fig.update_yaxes(
        gridcolor=_GRID, title_text="Value ($)", tickformat="$,.0f",
        row=1, col=1,
    )
    fig.update_yaxes(
        gridcolor=_GRID, title_text="Drawdown", ticksuffix="%",
        row=2, col=1,
    )
    fig.update_xaxes(gridcolor=_GRID, title_text="Candle", row=2, col=1)
    fig.update_xaxes(gridcolor=_GRID, showticklabels=False, row=1, col=1)
    return fig


def pnl_histogram(trades: List[Dict]) -> go.Figure:
    """Trade P&L distribution — green bars for wins, red for losses, mean line."""
    pnls = [t["pnl_pct"] * 100 for t in trades]
    wins = [p for p in pnls if p > 0]
    losses = [p for p in pnls if p <= 0]
    mean_pnl = statistics.mean(pnls) if pnls else 0.0

    fig = go.Figure()

    fig.add_trace(go.Histogram(
        x=losses,
        nbinsx=12,
        name="Loss",
        marker_color=_NEGATIVE,
        marker_line_color=_BG,
        marker_line_width=0.8,
        opacity=0.8,
        hovertemplate="P&L: %{x:.2f}%<br>Count: %{y}<extra>Loss</extra>",
    ))

    fig.add_trace(go.Histogram(
        x=wins,
        nbinsx=12,
        name="Win",
        marker_color=_POSITIVE,
        marker_line_color=_BG,
        marker_line_width=0.8,
        opacity=0.8,
        hovertemplate="P&L: %{x:.2f}%<br>Count: %{y}<extra>Win</extra>",
    ))

    # Zero line
    fig.add_vline(x=0, line_color=_ZERO, line_width=2)

    # Mean line
    fig.add_vline(
        x=mean_pnl,
        line_color=_ACCENT,
        line_width=1.5,
        line_dash="dash",
        annotation_text=f"Mean {mean_pnl:+.2f}%",
        annotation_position="top right" if mean_pnl >= 0 else "top left",
        annotation_font=dict(size=10, color=_ACCENT),
    )

    fig.update_layout(
        **_base_layout(
            height=300,
            title=dict(text="Trade P&L Distribution", font=dict(size=13, color=_TEXT2)),
        ),
        barmode="overlay",
        xaxis=dict(title="P&L %", gridcolor=_GRID, ticksuffix="%"),
        yaxis=dict(title="Trades", gridcolor=_GRID),
        legend=dict(
            orientation="h",
            x=1, y=1, xanchor="right", yanchor="bottom",
            font=dict(size=11),
            bgcolor="rgba(0,0,0,0)",
        ),
    )
    return fig
