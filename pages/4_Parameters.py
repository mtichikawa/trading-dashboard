"""Parameters — T4 sweep results, current config, and T3↔T4 feedback loop."""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.data_loader import load_backtest_result, synthetic_sweep_results

st.set_page_config(page_title="Parameters", page_icon="⚙️", layout="wide")

st.markdown("""
<style>
.section-label {
    font-size: 10px; font-weight: 700; letter-spacing: 0.2em;
    text-transform: uppercase; color: #6cc0e0; margin-bottom: 4px;
}
.config-box {
    background: rgba(26,35,50,0.7);
    border: 1px solid #3a6888;
    border-radius: 8px;
    padding: 20px 24px;
}
.config-param { font-size: 14px; margin-bottom: 10px; color: #e8eef4; }
.config-param code { background: rgba(108,192,224,0.15); color: #6cc0e0; padding: 2px 8px; border-radius: 4px; font-size: 13px; }
.config-label { color: #90b0c8; }
.best-badge {
    display: inline-block;
    background: rgba(76,175,125,0.2);
    border: 1px solid #4caf7d;
    color: #4caf7d;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 2px 8px;
    border-radius: 4px;
    margin-left: 8px;
}
.loop-box {
    background: rgba(26,35,50,0.6);
    border-left: 3px solid #6cc0e0;
    border-radius: 0 6px 6px 0;
    padding: 18px 24px;
    color: #a0c0d8;
    font-size: 13.5px;
    line-height: 1.85;
}
.loop-box strong { color: #e8eef4; }
.stage-box {
    background: rgba(26,35,50,0.5);
    border: 1px solid #2a3a4a;
    border-radius: 6px;
    padding: 14px 16px;
    height: 100%;
}
.stage-num { font-size: 11px; font-weight: 700; color: #6cc0e0; letter-spacing: 0.15em; text-transform: uppercase; }
.stage-title { font-size: 14px; font-weight: 600; color: #e8eef4; margin: 4px 0; }
.stage-desc { font-size: 12px; color: #90b0c8; line-height: 1.6; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="section-label">T4 → T3 Feedback Loop</p>', unsafe_allow_html=True)
st.title("⚙️ Parameters")
st.markdown(
    "T4's parameter sweep finds the signal configuration that maximizes Sharpe ratio "
    "over the backtest window. The winning parameters are written back to T3 as defaults — "
    "closing the feedback loop between signal generation and strategy evaluation."
)

st.markdown("---")

result = load_backtest_result()
params = result["parameters"]
metrics = result["metrics"]

# ── CURRENT CONFIG ────────────────────────────────────────────────────────────
st.markdown('<p class="section-label">Current Configuration</p>', unsafe_allow_html=True)
st.markdown("&nbsp;")

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
<div class="config-box">
<div style="font-size:12px; color:#7098b0; text-transform:uppercase; letter-spacing:0.12em; margin-bottom:14px;">
T3 Signal Weights
</div>
<div class="config-param"><span class="config-label">Technical weight</span> &nbsp; <code>{params.get('tech_weight', 0.6)}</code></div>
<div class="config-param"><span class="config-label">Sentiment weight</span> &nbsp; <code>{params.get('sent_weight', 0.4)}</code></div>
<div style="font-size:12px; color:#506070; margin-top:8px;">
Fusion: signal = 0.6 × technical + 0.4 × sentiment
</div>
</div>
""", unsafe_allow_html=True)

with col2:
    sl = params.get('stop_loss_pct', 0.02)
    st.markdown(f"""
<div class="config-box">
<div style="font-size:12px; color:#7098b0; text-transform:uppercase; letter-spacing:0.12em; margin-bottom:14px;">
T4 Strategy Parameters
</div>
<div class="config-param"><span class="config-label">Entry threshold</span> &nbsp; <code>|signal| &gt; {params.get('signal_threshold', 0.1)}</code></div>
<div class="config-param"><span class="config-label">Stop loss</span> &nbsp; <code>{sl:.0%} per trade</code></div>
<div style="font-size:12px; color:#506070; margin-top:8px;">
Position closes on signal reversal or stop-loss trigger.
</div>
</div>
""", unsafe_allow_html=True)

st.markdown("&nbsp;")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Sharpe (current config)", f"{metrics['sharpe_ratio']:.2f}")
c2.metric("Sortino", f"{metrics['sortino_ratio']:.2f}")
c3.metric("Win Rate", f"{metrics['win_rate']:.1%}")
c4.metric("Total Return", f"{metrics['total_return_pct']:+.2f}%")

st.markdown("---")

# ── SWEEP METHODOLOGY ────────────────────────────────────────────────────────
st.markdown('<p class="section-label">Sweep Methodology</p>', unsafe_allow_html=True)
st.markdown("&nbsp;")

st.markdown("""
<div class="loop-box">
Exhaustive grid search across all parameters would require 17,000+ combinations — most of which share similar characteristics.
T4 uses a <strong>3-stage staged sweep</strong> that narrows the search space at each step, testing ~60–80 configs total
while still exploring the key tradeoffs.
</div>
""", unsafe_allow_html=True)

st.markdown("&nbsp;")

s1, s2, s3 = st.columns(3)
with s1:
    st.markdown("""
<div class="stage-box">
<div class="stage-num">Stage 1</div>
<div class="stage-title">Fusion Weights</div>
<div class="stage-desc">
Test technical/sentiment weight ratios from 0.3/0.7 to 0.8/0.2 with default indicator parameters.
Find the weight balance that produces the best Sharpe ratio.
</div>
</div>
""", unsafe_allow_html=True)
with s2:
    st.markdown("""
<div class="stage-box">
<div class="stage-num">Stage 2</div>
<div class="stage-title">Indicator Parameters</div>
<div class="stage-desc">
Using the best weight from Stage 1, sweep EMA fast/slow periods, RSI period, and Bollinger window.
Fine-tune the technical path.
</div>
</div>
""", unsafe_allow_html=True)
with s3:
    st.markdown("""
<div class="stage-box">
<div class="stage-num">Stage 3</div>
<div class="stage-title">Entry Thresholds</div>
<div class="stage-desc">
Using best weight + indicators, sweep signal entry threshold and stop-loss level.
Calibrate trade selectivity and risk limits.
</div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ── SWEEP RESULTS ────────────────────────────────────────────────────────────
st.markdown('<p class="section-label">Sweep Results — Ranked by Sharpe</p>', unsafe_allow_html=True)
st.markdown("&nbsp;")

df = synthetic_sweep_results()

def highlight_best(row):
    if row.name == 0:
        return ["background-color: rgba(76,175,125,0.15); border-left: 3px solid #4caf7d"] * len(row)
    return [""] * len(row)

styled = df.style.apply(highlight_best, axis=1).format({
    "sharpe": "{:.2f}",
    "sortino": "{:.2f}",
    "tech_weight": "{:.1f}",
    "sent_weight": "{:.1f}",
    "signal_threshold": "{:.2f}",
})

st.dataframe(styled, use_container_width=True, hide_index=True)
st.caption("Row 1 (highlighted) is the current active configuration.")

st.markdown("---")

# ── FEEDBACK LOOP ────────────────────────────────────────────────────────────
st.markdown('<p class="section-label">The Feedback Loop</p>', unsafe_allow_html=True)
st.markdown("&nbsp;")

st.markdown("""
<div class="loop-box">
<strong>T3 generates signals</strong> using its current parameter defaults.<br>
<strong>T4 backtests those signals</strong> against historical OHLCV data and runs the staged parameter sweep.<br>
<strong>T4 writes parameter_report.json</strong> — the winning configuration — to its results directory.<br>
<strong>T3 reads parameter_report.json</strong> on next run and updates its defaults.<br>
<strong>T5 (this dashboard)</strong> shows you the sweep results so you can review and approve before the loop closes.<br><br>
The system self-optimizes. You stay in the loop as the decision-maker.
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.caption("Sweep results shown are synthetic — live results written by T4 parameter_sweep.py when connected to T1 database")
