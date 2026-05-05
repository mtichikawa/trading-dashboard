"""Trading Arc Dashboard — home page.

Overview of the T1-T5 end-to-end paper trading system. The four sub-pages
(Signal Pipeline, Backtesting, Performance, Parameters) deep-dive into the
specific components.
"""

import streamlit as st

from src.style import inject_css, sidebar_links

st.set_page_config(
    page_title="Trading Arc Dashboard",
    page_icon="📈",
    layout="wide",
)
inject_css()
sidebar_links()

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown('<p class="section-label">Portfolio · Solo build</p>', unsafe_allow_html=True)
st.title("Trading Arc Dashboard")
st.markdown(
    "End-to-end paper trading system. Live market data, automated chart generation, "
    "dual-path signal analysis (technical indicators plus FinBERT sentiment), backtesting, "
    "and this oversight dashboard. Five repositories, free to run."
)

st.markdown("---")

# ── PIPELINE ──────────────────────────────────────────────────────────────────
st.markdown('<p class="section-label">The Arc</p>', unsafe_allow_html=True)
st.markdown("&nbsp;")

nodes = [
    ("T1", "crypto-data-pipeline",
     "Live OHLCV ingestion for BTC, ETH, and SOL via ccxt/Kraken. Stores to PostgreSQL with market event tagging and news headline logging.",
     "Shipped Mar 6", None),
    ("T2", "trading-chart-generator",
     "Reads T1 data and generates mplfinance candlestick PNGs with JSON sidecars containing OHLCV summary stats.",
     "Shipped Mar 10", "43/43 tests"),
    ("T3", "trading-signal-engine",
     "Dual-path signal engine: technical indicators (EMA, RSI, MACD, Bollinger) fused 60/40 with local FinBERT sentiment. Outputs signal JSON consumed by T4.",
     "Shipped Mar 16", "51/51 tests"),
    ("T4", "trading-backtester",
     "Backtests T3 signals against OHLCV history. Sharpe, Sortino, max drawdown. Staged parameter sweep feeds optimal weights back to T3.",
     "Shipped Mar 26", "72/72 tests"),
    ("T5", "trading-dashboard",
     "This app. Reviews signal output, backtest results, and parameter configurations across the full arc.",
     "Shipped Mar 31", "8/8 tests"),
]

cols = st.columns(5)
for col, (tag, name, desc, date, tests) in zip(cols, nodes):
    tests_html = f'<div class="node-tests">✓ {tests}</div>' if tests else ""
    with col:
        st.markdown(
            f"""
            <div class="pipeline-node live">
                <div class="node-badge">{tag}</div>
                <div class="node-name">{name}</div>
                <div class="node-desc">{desc}</div>
                <div class="node-tests">{date}</div>
                {tests_html}
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("&nbsp;")
st.markdown("&nbsp;")

# ── STATS ─────────────────────────────────────────────────────────────────────
stats = [
    ("5", "Repositories"),
    ("174", "Tests Passing"),
    ("3", "Pairs Tracked"),
    ("4", "Signal Indicators"),
    ("$0", "Monthly Cost"),
]
cols = st.columns(5)
for col, (num, label) in zip(cols, stats):
    with col:
        st.markdown(
            f'<div class="stat-box">'
            f'<div class="stat-num">{num}</div>'
            f'<div class="stat-label">{label}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

st.markdown("---")

# ── FEEDBACK LOOP ─────────────────────────────────────────────────────────────
st.markdown('<p class="section-label">The Feedback Loop</p>', unsafe_allow_html=True)
st.markdown("&nbsp;")
st.markdown(
    """
    <div class="loop-box">
    T4 records whether each T3 signal configuration led to a winning or losing paper trade.
    T3's parameters — indicator thresholds, sentiment weights, fusion ratio — tune from those
    outcomes. <strong>T5 (this dashboard) surfaces signal performance and lets you review
    parameter changes before they're applied. The system improves its own signal generation.
    You stay in the loop as the decision-maker.</strong>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

# ── NAVIGATION ────────────────────────────────────────────────────────────────
st.markdown('<p class="section-label">Explore</p>', unsafe_allow_html=True)
st.markdown("&nbsp;")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("**📡 Signal Pipeline**")
    st.markdown(
        "How T1–T3 generate a trading signal. Indicator breakdown, sentiment path, and fusion math shown for each pair."
    )
with col2:
    st.markdown("**📊 Backtesting**")
    st.markdown(
        "T4 equity curve, performance metrics, and trade log. What happened when T3's signals ran against historical price data."
    )
with col3:
    st.markdown("**📈 Performance**")
    st.markdown(
        "Drawdown analysis, returns distribution, and win/loss breakdown. Risk-adjusted view of the strategy."
    )
with col4:
    st.markdown("**⚙️ Parameters**")
    st.markdown(
        "Current signal configuration and parameter sweep results. The T3↔T4 feedback loop in detail."
    )

st.markdown("---")
st.caption(
    "Data sourced from local T3/T4 output files · falls back to synthetic data when live files unavailable · "
    "no paid APIs · [github.com/mtichikawa](https://github.com/mtichikawa)"
)
