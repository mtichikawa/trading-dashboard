"""Live Signals page — T3 signal output per pair/timeframe."""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.data_loader import load_latest_signals, signals_to_dataframe

st.set_page_config(page_title="Live Signals", page_icon="📡", layout="wide")
st.title("📡 Live Signals")
st.caption("Latest signal output from the T3 trading-signal-engine")

signals = load_latest_signals()
df = signals_to_dataframe(signals)

# Signal summary cards
cols = st.columns(len(signals))
for col, s in zip(cols, signals):
    with col:
        direction = "BUY" if s["signal"] > 0.1 else "SELL" if s["signal"] < -0.1 else "HOLD"
        color = "green" if direction == "BUY" else "red" if direction == "SELL" else "gray"
        st.metric(
            label=f"{s['pair']} ({s['timeframe']})",
            value=direction,
            delta=f"signal {s['signal']:+.4f}  conf {s['confidence']:.2f}",
        )

st.markdown("---")

st.subheader("Signal Breakdown")
st.dataframe(
    df[["pair", "timeframe", "signal", "confidence", "technical", "sentiment",
        "ema", "rsi", "macd", "bollinger"]],
    use_container_width=True,
)

st.markdown("---")
st.subheader("Indicator Detail")
for s in signals:
    with st.expander(f"{s['pair']} {s['timeframe']}"):
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("EMA Crossover", f"{s['indicators']['ema_crossover']:+.4f}")
        c2.metric("RSI", f"{s['indicators']['rsi']:+.4f}")
        c3.metric("MACD", f"{s['indicators']['macd']:+.4f}")
        c4.metric("Bollinger", f"{s['indicators']['bollinger']:+.4f}")
        st.caption(
            f"Technical: {s['technical_score']:+.4f}  |  "
            f"Sentiment: {s['sentiment_score']:+.4f}  |  "
            f"Fused (0.6/0.4): {s['signal']:+.4f}"
        )
