"""Backtesting — T4 results: equity curve, metrics, and trade log."""

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.charts import equity_curve_chart, pnl_histogram
from src.data_loader import load_backtest_result

st.set_page_config(page_title="Backtesting", page_icon="📊", layout="wide")

st.markdown("""
<style>
.section-label {
    font-size: 10px; font-weight: 700; letter-spacing: 0.2em;
    text-transform: uppercase; color: #6cc0e0; margin-bottom: 4px;
}
.explainer {
    background: rgba(26,35,50,0.5);
    border-left: 3px solid #3a6888;
    border-radius: 0 6px 6px 0;
    padding: 14px 18px;
    color: #90b0c8;
    font-size: 13px;
    line-height: 1.7;
}
.explainer strong { color: #e8eef4; }
.metric-card {
    background: rgba(26,35,50,0.7);
    border: 1px solid #3a6888;
    border-radius: 8px;
    padding: 16px;
    text-align: center;
}
.metric-val { font-size: 26px; font-weight: 700; color: #6cc0e0; }
.metric-lbl { font-size: 11px; color: #7098b0; text-transform: uppercase; letter-spacing: 0.1em; margin-top: 4px; }
</style>
""", unsafe_allow_html=True)

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
        config={"displayModeBar": False},
    )
    st.markdown("&nbsp;")
    st.markdown('<p class="section-label">P&L Distribution</p>', unsafe_allow_html=True)
    st.plotly_chart(
        pnl_histogram(trades),
        use_container_width=True,
        config={"displayModeBar": False},
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
st.caption("Results from T4 trading-backtester · synthetic data shown when live result files unavailable")
