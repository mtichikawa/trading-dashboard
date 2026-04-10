"""Signal Pipeline — T1 through T3 explained and visualized."""



from pathlib import Path

import sys



import streamlit as st



sys.path.insert(0, str(Path(__file__).parent.parent))

from src.charts import indicator_bar_chart

from src.data_loader import load_latest_signals



st.set_page_config(page_title="Signal Pipeline", page_icon="📡", layout="wide")



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

    height: 100%;

}

.explainer strong { color: #e8eef4; }

.fusion-math {

    font-family: monospace;

    font-size: 13px;

    color: #6cc0e0;

    background: rgba(26,35,50,0.8);

    padding: 10px 16px;

    border-radius: 6px;

    margin: 8px 0;

    line-height: 2;

}

.signal-header {

    background: rgba(26,35,50,0.7);

    border: 1px solid #3a6888;

    border-radius: 8px;

    padding: 20px;

    margin-bottom: 24px;

}

.signal-header.bullish { border-color: #4caf7d; }

.signal-header.bearish { border-color: #e05050; }

.signal-header.neutral { border-color: #7098b0; }

.direction { font-size: 22px; font-weight: 700; }

.direction.bullish { color: #4caf7d; }

.direction.bearish { color: #e05050; }

.direction.neutral { color: #90b0c8; }

</style>

""", unsafe_allow_html=True)



st.markdown('<p class="section-label">T1 → T2 → T3</p>', unsafe_allow_html=True)

st.title("📡 Signal Pipeline")

st.markdown(

    "How the arc converts raw market data into a single actionable signal — "

    "from price ingestion through indicator calculation to final fused output."

)



st.markdown("---")



# ── HOW IT WORKS ──────────────────────────────────────────────────────────────

st.markdown('<p class="section-label">How It Works</p>', unsafe_allow_html=True)

st.markdown("&nbsp;")



col1, col2, col3 = st.columns(3)

with col1:

    st.markdown("""

<div class="explainer">

<strong>T1 — Data Ingestion</strong><br><br>

Live OHLCV bars for BTC, ETH, and SOL are fetched from Kraken via ccxt and stored in PostgreSQL.

Market events (volume spikes, large candles) are tagged. News headlines are logged for the sentiment path.

</div>

""", unsafe_allow_html=True)

with col2:

    st.markdown("""

<div class="explainer">

<strong>T2 — Chart Generation</strong><br><br>

For each bar set, T2 reads T1's database and renders an mplfinance candlestick chart.

Each chart gets a JSON sidecar with OHLCV summary stats — consumed by T3's vision demo mode.

</div>

""", unsafe_allow_html=True)

with col3:

    st.markdown("""

<div class="explainer">

<strong>T3 — Signal Engine</strong><br><br>

Two paths run in parallel: <strong>technical indicators</strong> (EMA crossover, RSI, MACD, Bollinger Bands)

and <strong>local FinBERT sentiment</strong> on recent headlines. Scores are fused 60/40 into a final signal.

</div>

""", unsafe_allow_html=True)



st.markdown("&nbsp;")

st.markdown("&nbsp;")



# ── FUSION MATH ───────────────────────────────────────────────────────────────

st.markdown('<p class="section-label">The Fusion Formula</p>', unsafe_allow_html=True)

st.markdown("&nbsp;")



col1, col2 = st.columns([1, 1])

with col1:

    st.markdown("""

<div class="fusion-math">

signal &nbsp;&nbsp;&nbsp;= 0.6 × technical_score + 0.4 × sentiment_score<br>

confidence = 1.0 − |technical_score − sentiment_score|

</div>

""", unsafe_allow_html=True)

with col2:

    st.markdown("""

**Signal range:** −1.0 (strong sell) → +1.0 (strong buy)



**Confidence** is highest when both paths agree, lowest when they diverge.

A high-confidence BUY means technical indicators and sentiment are both positive.



**Trade entry threshold:** |signal| > 0.1

""")



st.markdown("---")



# ── CURRENT SIGNALS ──────────────────────────────────────────────────────────

st.markdown('<p class="section-label">Current Signal Output</p>', unsafe_allow_html=True)

st.markdown("&nbsp;")



signals = load_latest_signals()



for s in signals:

    sig = s["signal"]

    conf = s["confidence"]

    tech = s["technical_score"]

    sent = s["sentiment_score"]

    ind = s["indicators"]



    if sig > 0.1:

        direction, css = "▲ BUY", "bullish"

    elif sig < -0.1:

        direction, css = "▼ SELL", "bearish"

    else:

        direction, css = "◆ HOLD", "neutral"



    st.markdown(f'<div class="signal-header {css}">', unsafe_allow_html=True)



    col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])

    with col1:

        st.markdown(f"### {s['pair']}")

        st.markdown(f"`{s['timeframe']} timeframe`")

        st.markdown(

            f'<span class="direction {css}">{direction}</span>',

            unsafe_allow_html=True,

        )

    with col2:

        st.metric("Signal", f"{sig:+.4f}")

    with col3:

        st.metric("Confidence", f"{conf:.2f}")

    with col4:

        st.metric("Technical", f"{tech:+.3f}")

    with col5:

        st.metric("Sentiment", f"{sent:+.3f}")



    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("&nbsp;")



    # Chart + legend side by side

    chart_col, legend_col = st.columns([2, 1])

    with chart_col:

        st.plotly_chart(

            indicator_bar_chart(s, title="Indicator Breakdown"),

            use_container_width=True,

            config={"displayModeBar": "hover", "displaylogo": False, "doubleClick": "reset+autosize"},

        )

    with legend_col:

        st.markdown("**What each indicator measures**")

        st.markdown("&nbsp;")

        indicator_notes = [

            ("EMA Crossover", ind["ema_crossover"],

             "Positive when the fast EMA (12-period) is above the slow EMA (26-period). Measures trend direction."),

            ("RSI (14)", ind["rsi"],

             "Relative Strength Index, normalized to −1/+1. Negative suggests oversold; positive suggests overbought."),

            ("MACD", ind["macd"],

             "+1 on a bullish signal line crossover, −1 on bearish. Captures momentum shifts."),

            ("Bollinger Bands", ind["bollinger"],

             "Price position relative to the 2σ bands. +1 at upper band (extended), −1 at lower band."),

        ]

        for name, val, note in indicator_notes:

            color = "#4caf7d" if val >= 0 else "#e05050"

            st.markdown(

                f"**{name}:** <span style='color:{color}'>{val:+.4f}</span>",

                unsafe_allow_html=True,

            )

            st.caption(note)

            st.markdown("")



    st.markdown("---")



st.caption("Signals sourced from T3 output files · synthetic data shown when live files unavailable")

