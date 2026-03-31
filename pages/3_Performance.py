"""Performance page — equity curve and risk metrics."""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.data_loader import load_backtest_result

st.set_page_config(page_title="Performance", page_icon="📊", layout="wide")
st.title("📊 Performance")
st.caption("Risk-adjusted return metrics and equity curve from T4 backtesting")

result = load_backtest_result()
metrics = result["metrics"]

# Risk metrics
st.subheader("Risk Metrics")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Sharpe Ratio", f"{metrics['sharpe_ratio']:.2f}")
c2.metric("Sortino Ratio", f"{metrics['sortino_ratio']:.2f}")
c3.metric("Max Drawdown", f"{metrics['max_drawdown_pct']:.2f}%")
c4.metric("Total Return", f"{metrics['total_return_pct']:+.2f}%")

st.markdown("---")

# Equity curve — Plotly chart added Thu Apr 2
st.subheader("Equity Curve")
st.info("Interactive Plotly equity curve and drawdown chart — coming Thu Apr 2.")

equity = result["equity_curve"]
import pandas as pd
df = pd.DataFrame({"equity": equity})
st.line_chart(df, use_container_width=True)
