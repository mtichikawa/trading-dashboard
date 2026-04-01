"""Performance — deep dive into risk metrics, drawdown, and trade analysis."""

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.charts import equity_with_drawdown, pnl_histogram
from src.data_loader import load_backtest_result

st.set_page_config(page_title="Performance", page_icon="📈", layout="wide")

st.markdown("""
<style>
.section-label {
    font-size: 10px; font-weight: 700; letter-spacing: 0.2em;
    text-transform: uppercase; color: #6cc0e0; margin-bottom: 4px;
}
.metric-card {
    background: rgba(26,35,50,0.7);
    border: 1px solid #3a6888;
    border-radius: 8px;
    padding: 16px;
    text-align: center;
}
.metric-val { font-size: 26px; font-weight: 700; color: #6cc0e0; }
.metric-val.positive { color: #4caf7d; }
.metric-val.negative { color: #e05050; }
.metric-lbl { font-size: 11px; color: #7098b0; text-transform: uppercase; letter-spacing: 0.1em; margin-top: 4px; }
.metric-note { font-size: 10px; color: #506070; margin-top: 2px; }
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
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="section-label">T4 — Risk Analysis</p>', unsafe_allow_html=True)
st.title("📈 Performance")
st.markdown(
    "Risk-adjusted metrics, equity curve, drawdown analysis, and trade breakdown "
    "from the T4 backtester running T3's signals against historical OHLCV data."
)

st.markdown("---")

result = load_backtest_result()
metrics = result["metrics"]
trades = result["trades"]
equity = result["equity_curve"]

wins = [t for t in trades if t["pnl_pct"] > 0]
losses = [t for t in trades if t["pnl_pct"] <= 0]
avg_win = sum(t["pnl_pct"] for t in wins) / len(wins) * 100 if wins else 0
avg_loss = sum(t["pnl_pct"] for t in losses) / len(losses) * 100 if losses else 0

# ── METRICS ──────────────────────────────────────────────────────────────────
st.markdown('<p class="section-label">Risk-Adjusted Metrics</p>', unsafe_allow_html=True)
st.markdown("&nbsp;")

cols = st.columns(6)
metric_defs = [
    ("Sharpe Ratio", f"{metrics['sharpe_ratio']:.2f}", "Annualized · rf=0", "neutral"),
    ("Sortino Ratio", f"{metrics['sortino_ratio']:.2f}", "Downside deviation only", "neutral"),
    ("Max Drawdown", f"{metrics['max_drawdown_pct']:.2f}%", "Peak-to-trough decline", "negative"),
    ("Total Return", f"{metrics['total_return_pct']:+.2f}%", "Over backtest period", "positive"),
    ("Avg Win", f"{avg_win:+.2f}%", "Per winning trade", "positive"),
    ("Avg Loss", f"{avg_loss:+.2f}%", "Per losing trade", "negative"),
]
for col, (label, val, note, cls) in zip(cols, metric_defs):
    with col:
        st.markdown(
            f'<div class="metric-card">'
            f'<div class="metric-val {cls}">{val}</div>'
            f'<div class="metric-lbl">{label}</div>'
            f'<div class="metric-note">{note}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

st.markdown("&nbsp;")

# ── WHAT THESE MEAN ──────────────────────────────────────────────────────────
with st.expander("What do these metrics mean?"):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
<div class="explainer">
<strong>Sharpe Ratio</strong> — excess return per unit of total volatility.
Above 1.0 is generally considered good; above 2.0 is excellent.
Annualized here assuming hourly candles (8,760 periods/year).<br><br>
<strong>Sortino Ratio</strong> — like Sharpe but only penalizes downside volatility.
Higher than Sharpe means losses are less volatile than gains — a good sign.
</div>
""", unsafe_allow_html=True)
    with col2:
        st.markdown("""
<div class="explainer">
<strong>Max Drawdown</strong> — the worst peak-to-trough decline in portfolio value.
A lower number means the strategy avoids large losing streaks.
This is often the metric that matters most in practice.<br><br>
<strong>Profit Factor</strong> — gross profit divided by gross loss.
Above 1.0 means the strategy makes more than it loses in total.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ── EQUITY + DRAWDOWN ────────────────────────────────────────────────────────
st.markdown('<p class="section-label">Equity Curve & Drawdown</p>', unsafe_allow_html=True)
st.plotly_chart(
    equity_with_drawdown(equity),
    use_container_width=True,
    config={"displayModeBar": False},
)

st.markdown("---")

# ── TRADE BREAKDOWN ──────────────────────────────────────────────────────────
st.markdown('<p class="section-label">Trade Breakdown</p>', unsafe_allow_html=True)
st.markdown("&nbsp;")

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.plotly_chart(
        pnl_histogram(trades),
        use_container_width=True,
        config={"displayModeBar": False},
    )

with col2:
    st.markdown("**Win / Loss**")
    st.markdown("&nbsp;")
    total = len(trades)
    win_count = len(wins)
    loss_count = len(losses)
    st.markdown(f"**Total trades:** {total}")
    st.markdown(f"**Wins:** {win_count} ({win_count/total:.0%})")
    st.markdown(f"**Losses:** {loss_count} ({loss_count/total:.0%})")
    st.markdown(f"**Profit factor:** {metrics['profit_factor']:.2f}")
    st.markdown(f"**Avg win:** {avg_win:+.2f}%")
    st.markdown(f"**Avg loss:** {avg_loss:+.2f}%")

with col3:
    st.markdown("**By Side**")
    st.markdown("&nbsp;")
    longs = [t for t in trades if t["side"] == "long"]
    shorts = [t for t in trades if t["side"] == "short"]
    long_wins = [t for t in longs if t["pnl_pct"] > 0]
    short_wins = [t for t in shorts if t["pnl_pct"] > 0]
    st.markdown(f"**Long trades:** {len(longs)}")
    if longs:
        st.markdown(f"**Long win rate:** {len(long_wins)/len(longs):.0%}")
    st.markdown(f"**Short trades:** {len(shorts)}")
    if shorts:
        st.markdown(f"**Short win rate:** {len(short_wins)/len(shorts):.0%}")
    avg_bars = sum(t["bars_held"] for t in trades) / len(trades) if trades else 0
    st.markdown(f"**Avg hold time:** {avg_bars:.1f} bars")

st.markdown("---")
st.caption("Results from T4 trading-backtester · synthetic data shown when live result files unavailable")
