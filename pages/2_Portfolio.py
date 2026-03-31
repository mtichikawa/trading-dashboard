"""Portfolio page — T4 backtest result summary."""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.data_loader import load_backtest_result

st.set_page_config(page_title="Portfolio", page_icon="💼", layout="wide")
st.title("💼 Portfolio")
st.caption("Position and trade summary from the T4 trading-backtester")

result = load_backtest_result()
metrics = result["metrics"]
params = result["parameters"]
trades = result["trades"]

# Top-level metrics
st.subheader("Summary")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Return", f"{metrics['total_return_pct']:+.2f}%")
c2.metric("Total Trades", metrics["total_trades"])
c3.metric("Win Rate", f"{metrics['win_rate']:.1%}")
c4.metric("Profit Factor", f"{metrics['profit_factor']:.2f}")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Active Parameters")
    for k, v in params.items():
        st.markdown(f"**{k}:** `{v}`")

with col2:
    st.subheader("Recent Trades")
    if trades:
        import pandas as pd
        df = pd.DataFrame(trades[-10:])
        df["pnl_pct"] = df["pnl_pct"].map(lambda x: f"{x:+.2%}")
        st.dataframe(df[["side", "entry_price", "exit_price", "pnl_pct", "bars_held"]],
                     use_container_width=True)
    else:
        st.info("No trades recorded.")
