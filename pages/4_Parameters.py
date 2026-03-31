"""Parameters page — T4 sweep results and T3 weight review."""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.data_loader import load_backtest_result

st.set_page_config(page_title="Parameters", page_icon="⚙️", layout="wide")
st.title("⚙️ Parameters")
st.caption("T4 parameter sweep results and current T3 signal weight configuration")

result = load_backtest_result()
params = result["parameters"]
metrics = result["metrics"]

st.subheader("Current Configuration")
col1, col2 = st.columns(2)

with col1:
    st.markdown("**T3 Signal Weights**")
    st.markdown(f"- Technical weight: `{params.get('tech_weight', 0.6)}`")
    st.markdown(f"- Sentiment weight: `{params.get('sent_weight', 0.4)}`")

with col2:
    st.markdown("**T4 Strategy Parameters**")
    st.markdown(f"- Signal threshold: `{params.get('signal_threshold', 0.1)}`")
    st.markdown(f"- Stop loss: `{params.get('stop_loss_pct', 0.02):.1%}`")

st.markdown("---")
st.subheader("Resulting Metrics")
c1, c2, c3 = st.columns(3)
c1.metric("Sharpe", f"{metrics['sharpe_ratio']:.2f}")
c2.metric("Win Rate", f"{metrics['win_rate']:.1%}")
c3.metric("Return", f"{metrics['total_return_pct']:+.2f}%")

st.markdown("---")
st.info("Full parameter sweep table and sensitivity heatmap — coming Thu Apr 2.")
