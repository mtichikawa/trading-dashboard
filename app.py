"""Trading Arc Dashboard — Home

One-stop overview of the T1-T5 end-to-end paper trading system.
"""

import streamlit as st

st.set_page_config(
    page_title="Trading Arc Dashboard",
    page_icon="📈",
    layout="wide",
)

st.markdown("""
<style>
.pipeline-node {
    background: rgba(26,35,50,0.7);
    border: 1px solid #3a6888;
    border-radius: 8px;
    padding: 18px 12px;
    text-align: center;
    height: 100%;
    min-height: 160px;
    display: flex;
    flex-direction: column;
    gap: 8px;
}
.pipeline-node.live { border-color: #4caf7d; }
.node-badge {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #6cc0e0;
}
.node-name {
    font-size: 12px;
    font-weight: 600;
    color: #e8eef4;
    font-family: monospace;
}
.node-desc {
    font-size: 11.5px;
    color: #90b0c8;
    line-height: 1.55;
    flex: 1;
}
.node-tests {
    font-size: 10px;
    color: #4caf7d;
    letter-spacing: 0.08em;
}
.stat-box { text-align: center; padding: 16px 8px; }
.stat-num { font-size: 32px; font-weight: 700; color: #6cc0e0; line-height: 1; }
.stat-label { font-size: 11px; color: #7098b0; text-transform: uppercase; letter-spacing: 0.12em; margin-top: 6px; }
.loop-box {
    background: rgba(26,35,50,0.6);
    border-left: 3px solid #6cc0e0;
    border-radius: 0 6px 6px 0;
    padding: 18px 24px;
    line-height: 1.8;
    color: #a0c0d8;
    font-size: 14px;
}
.loop-box strong { color: #e8eef4; }
.section-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #6cc0e0;
    margin-bottom: 4px;
}
</style>
""", unsafe_allow_html=True)

# ── HEADER ──────────────────────────────────────────────────────────────────
st.markdown('<p class="section-label">Portfolio Project</p>', unsafe_allow_html=True)
st.title("Trading Arc Dashboard")
st.markdown(
    "An end-to-end paper trading system: live market data ingestion, "
    "automated chart generation, dual-path signal analysis, backtesting, "
    "and this oversight dashboard. Five repositories. Entirely free to run."
)

st.markdown("---")

# ── PIPELINE ────────────────────────────────────────────────────────────────
st.markdown('<p class="section-label">The Arc</p>', unsafe_allow_html=True)
st.markdown("&nbsp;")

nodes = [
    ("T1", "crypto-data-pipeline",
     "Live OHLCV ingestion for BTC, ETH, and SOL via ccxt/Kraken. Stores to PostgreSQL with market event tagging and news headline logging.",
     "Shipped Mar 6", None),
    ("T2", "trading-chart-generator",
     "Reads T1 data and generates mplfinance candlestick PNGs with JSON sidecars containing OHLCV summary stats.",
     "Shipped Mar 10", "25/25 tests"),
    ("T3", "trading-signal-engine",
     "Dual-path signal engine: technical indicators (EMA, RSI, MACD, Bollinger) fused 60/40 with local FinBERT sentiment. Outputs signal JSON consumed by T4.",
     "Shipped Mar 16", "51/51 tests"),
    ("T4", "trading-backtester",
     "Backtests T3 signals against OHLCV history. Computes Sharpe, Sortino, max drawdown. Staged parameter sweep feeds optimal weights back to T3.",
     "Shipped Mar 26", "72/72 tests"),
    ("T5", "trading-dashboard",
     "This app. Reviews signal output, backtest results, and parameter configurations across the full arc.",
     "Shipped Mar 31", "8/8 tests"),
]

cols = st.columns(5)
for col, (tag, name, desc, date, tests) in zip(cols, nodes):
    tests_html = f'<div class="node-tests">✓ {tests}</div>' if tests else ""
    with col:
        st.markdown(f"""
        <div class="pipeline-node live">
            <div class="node-badge">{tag}</div>
            <div class="node-name">{name}</div>
            <div class="node-desc">{desc}</div>
            <div class="node-tests">{date}</div>
            {tests_html}
        </div>
        """, unsafe_allow_html=True)

st.markdown("&nbsp;")
st.markdown("&nbsp;")

# ── STATS ────────────────────────────────────────────────────────────────────
cols = st.columns(5)
stats = [("5", "Repositories"), ("156", "Tests Passing"), ("3", "Pairs Tracked"), ("4", "Signal Indicators"), ("$0", "Monthly Cost")]
for col, (num, label) in zip(cols, stats):
    with col:
        st.markdown(
            f'<div class="stat-box"><div class="stat-num">{num}</div>'
            f'<div class="stat-label">{label}</div></div>',
            unsafe_allow_html=True,
        )

st.markdown("---")

# ── FEEDBACK LOOP ────────────────────────────────────────────────────────────
st.markdown('<p class="section-label">The Feedback Loop</p>', unsafe_allow_html=True)
st.markdown("&nbsp;")
st.markdown("""
<div class="loop-box">
T4 records whether each T3 signal configuration led to a winning or losing paper trade.
T3's parameters — indicator thresholds, sentiment weights, fusion ratio — are tuned based on those outcomes.
<strong>T5 (this dashboard) surfaces signal performance and lets you review parameter changes before they're applied.
The system improves its own signal generation. You stay in the loop as the decision-maker.</strong>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ── NAVIGATION ───────────────────────────────────────────────────────────────
st.markdown('<p class="section-label">Explore</p>', unsafe_allow_html=True)
st.markdown("&nbsp;")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("**📡 Signal Pipeline**")
    st.markdown("How T1–T3 generate a trading signal. Indicator breakdown, sentiment path, and fusion math shown for each pair.", unsafe_allow_html=True)
with col2:
    st.markdown("**📊 Backtesting**")
    st.markdown("T4 equity curve, performance metrics, and trade log. What happened when T3's signals ran against historical price data.")
with col3:
    st.markdown("**📈 Performance**")
    st.markdown("Drawdown analysis, returns distribution, and win/loss breakdown. Risk-adjusted view of the strategy.")
with col4:
    st.markdown("**⚙️ Parameters**")
    st.markdown("Current signal configuration and parameter sweep results. The T3↔T4 feedback loop in detail.")

st.markdown("---")
st.caption(
    "Data sourced from local T3/T4 output files · falls back to synthetic data when live files unavailable · "
    "no paid APIs · [github.com/mtichikawa](https://github.com/mtichikawa)"
)
