"""Trading Arc Dashboard — Home

Overview of the T1-T5 end-to-end paper trading system.
"""

import streamlit as st

st.set_page_config(
    page_title="Trading Arc Dashboard",
    page_icon="📈",
    layout="wide",
)

st.title("Trading Arc Dashboard")
st.caption(
    "End-to-end paper trading system: live market data → chart generation"
    " → signal analysis → backtesting → oversight"
)

st.markdown("---")

col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("System Arc")
    arc_nodes = [
        ("T1", "crypto-data-pipeline", "Live OHLCV via ccxt/Kraken · PostgreSQL", "🟢 Live"),
        ("T2", "trading-chart-generator", "Candlestick PNGs + JSON sidecars · 25/25 tests", "🟢 Complete"),
        ("T3", "trading-signal-engine", "EMA/RSI/MACD/BB + FinBERT sentiment · 51/51 tests", "🟢 Complete"),
        ("T4", "trading-backtester", "pandas backtesting + parameter sweep · 72/72 tests", "🟢 Complete"),
        ("T5", "trading-dashboard", "Streamlit oversight UI · this app", "🟡 Active"),
    ]
    for tag, repo, desc, status in arc_nodes:
        st.markdown(f"**{tag} · {repo}** &nbsp; {status}  \n<small>{desc}</small>", unsafe_allow_html=True)
        st.markdown("")

with col2:
    st.subheader("Pages")
    st.markdown("""
**📡 Live Signals**
Latest T3 signal output per pair and timeframe

**💼 Portfolio**
Current position summary from T4 backtest results

**📊 Performance**
Equity curve, drawdown, and return metrics

**⚙️ Parameters**
T4 parameter sweep results and T3 weight review

Use the sidebar to navigate.
""")

st.markdown("---")
st.caption(
    "All data sourced from local T3/T4 output files. "
    "Falls back to synthetic data when live files are unavailable. "
    "Entirely free to run — no paid APIs."
)
