"""Backtesting — T4 results: equity curve, metrics, and trade log."""

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.charts import equity_curve_chart, pnl_histogram
from src.data_loader import load_backtest_result
from src.style import inject_css, sidebar_links

st.set_page_config(page_title="Backtesting", page_icon="📊", layout="wide")
inject_css()
sidebar_links()

st.markdown('<p class="section-label">T4 — trading-backtester</p>', unsafe_allow_html=True)
st.title("📊 Backtesting")
st.markdown(
    "T4 runs T3's signal output against historical OHLCV data. "
    "It enters and exits positions based on signal threshold and stop-loss rules, "
    "then computes risk-adjusted performance metrics."
)

st.markdown("---")

# ── HOW IT WORKS ──────────────────────────────────────────────────────────────
st.markdown('<p class="section-label">How It Works</p>', unsafe_allow_html=True)
st.markdown("&nbsp;")

st.markdown("""
<div class="explainer">
<strong>Signal → Trade:</strong> When the fused signal exceeds the entry threshold (|signal| > 0.1), T4 opens a long or short position.
The position closes when the signal reverses past the threshold or the stop-loss triggers (default 2%).
<br><br>
<strong>Parameter Sweep:</strong> T4 runs a staged grid search across signal thresholds, stop-loss levels, and T3 fusion weights.
The best-performing configuration (by Sharpe ratio) is surfaced in the Parameters page and fed back to T3.
<br><br>
<strong>Metrics:</strong> Sharpe and Sortino ratios are annualized assuming hourly candles (8,760 periods/year).
Max drawdown is the worst peak-to-trough decline in portfolio value.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

result = load_backtest_result()
metrics = result["metrics"]
params = result["parameters"]
trades = result["trades"]
equity = result["equity_curve"]

if result.get("is_synthetic", False):
    st.warning(
        "**Illustrative demo data, not a real or backtested track record.** "
        "No live backtest result files are available in this deployment, so the "
        "metrics below come from a fixed-seed synthetic generator and exist only "
        "to demonstrate the dashboard UI. Do not read them as trading performance.",
        icon="⚠️",
    )

# ── METRICS ──────────────────────────────────────────────────────────────────
st.markdown('<p class="section-label">Performance Metrics</p>', unsafe_allow_html=True)
st.markdown("&nbsp;")

m_cols = st.columns(7)
metric_items = [
    ("Total Return", f"{metrics['total_return_pct']:+.2f}%"),
    ("Sharpe Ratio", f"{metrics['sharpe_ratio']:.2f}"),
    ("Sortino Ratio", f"{metrics['sortino_ratio']:.2f}"),
    ("Max Drawdown", f"{metrics['max_drawdown_pct']:.2f}%"),
    ("Win Rate", f"{metrics['win_rate']:.1%}"),
    ("Profit Factor", f"{metrics['profit_factor']:.2f}"),
    ("Total Trades", str(metrics["total_trades"])),
]
for col, (label, val) in zip(m_cols, metric_items):
    with col:
        st.markdown(
            f'<div class="metric-card"><div class="metric-val">{val}</div>'
            f'<div class="metric-lbl">{label}</div></div>',
            unsafe_allow_html=True,
        )

st.markdown("&nbsp;")
st.markdown("---")

# ── EQUITY CURVE + TRADE LOG ──────────────────────────────────────────────────
chart_col, trades_col = st.columns([3, 2])

with chart_col:
    st.markdown('<p class="section-label">Equity Curve</p>', unsafe_allow_html=True)
    st.plotly_chart(
        equity_curve_chart(equity, title=""),
        use_container_width=True,
        config={"displayModeBar": "hover", "displaylogo": False, "doubleClick": "reset+autosize"},
    )
    st.markdown("&nbsp;")
    st.markdown('<p class="section-label">P&L Distribution</p>', unsafe_allow_html=True)
    st.plotly_chart(
        pnl_histogram(trades),
        use_container_width=True,
        config={"displayModeBar": "hover", "displaylogo": False, "doubleClick": "reset+autosize"},
    )

with trades_col:
    st.markdown('<p class="section-label">Recent Trades</p>', unsafe_allow_html=True)
    st.markdown("&nbsp;")
    if trades:
        df = pd.DataFrame(trades[-15:])
        df = df[::-1].reset_index(drop=True)
        df["side"] = df["side"].str.upper()
        df["pnl"] = df["pnl_pct"].map(lambda x: f"{x:+.2%}")
        df["entry"] = df["entry_price"].map(lambda x: f"${x:,.2f}")
        df["exit"] = df["exit_price"].map(lambda x: f"${x:,.2f}")
        df["bars"] = df["bars_held"]

        def color_row(row):
            color = "#1a3a2a" if "+" in row["pnl"] else "#3a1a1a"
            return [f"background-color: {color}"] * len(row)

        styled = df[["side", "entry", "exit", "pnl", "bars"]].style.apply(color_row, axis=1)
        st.dataframe(styled, use_container_width=True, height=520)
    else:
        st.info("No trades recorded.")

    st.markdown("---")
    st.markdown('<p class="section-label">Active Parameters</p>', unsafe_allow_html=True)
    st.markdown("&nbsp;")
    param_labels = {
        "signal_threshold": "Signal threshold",
        "stop_loss_pct": "Stop loss",
        "tech_weight": "Technical weight",
        "sent_weight": "Sentiment weight",
    }
    for k, label in param_labels.items():
        v = params.get(k, "—")
        display = f"{v:.1%}" if "pct" in k or "weight" in k else str(v)
        st.markdown(f"**{label}:** `{display}`")

st.markdown("---")
st.caption(
    "Illustrative synthetic demo data (fixed-seed generator) · not live or backtested performance"
    if result.get("is_synthetic", False) else
    "Results from T4 trading-backtester on historical OHLCV data"
)
