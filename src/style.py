"""Shared visual styling for the dashboard.

One source of truth for colors, fonts, and reusable component CSS.
Each page calls inject_css() once at the top (after st.set_page_config),
and sidebar_links() to add the portfolio + repo back-links.
"""

import streamlit as st


# ── Public API ────────────────────────────────────────────────────────────────

def inject_css() -> None:
    """Inject the dashboard's shared stylesheet."""
    st.markdown(_CSS, unsafe_allow_html=True)


def sidebar_links() -> None:
    """Append portfolio + repo back-links below Streamlit's page nav."""
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        "**[← mtichikawa.github.io](https://mtichikawa.github.io)**  \n"
        "[github.com/mtichikawa](https://github.com/mtichikawa)"
    )


# ── Stylesheet ────────────────────────────────────────────────────────────────

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500&family=DM+Serif+Display&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'DM Sans', -apple-system, sans-serif;
}

h1, h2, h3, h4 {
    font-family: 'DM Serif Display', Georgia, serif;
    font-weight: 400;
    letter-spacing: -0.005em;
}

/* ── Section label (mono uppercase, accent) ── */
.section-label {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #6cc0e0;
    margin-bottom: 6px;
}

/* ── Pipeline node card (home page) ── */
.pipeline-node {
    background: rgba(26, 35, 50, 0.7);
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
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #6cc0e0;
}
.node-name {
    font-family: 'DM Mono', monospace;
    font-size: 12px;
    font-weight: 500;
    color: #e8eef4;
}
.node-desc {
    font-size: 12px;
    color: #90b0c8;
    line-height: 1.55;
    flex: 1;
}
.node-tests {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: #4caf7d;
    letter-spacing: 0.04em;
}

/* ── Stat box (home page) ── */
.stat-box { text-align: center; padding: 16px 8px; }
.stat-num {
    font-family: 'DM Serif Display', serif;
    font-size: 36px;
    color: #6cc0e0;
    line-height: 1;
}
.stat-label {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: #7098b0;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    margin-top: 6px;
}

/* ── Loop box (feedback callout) ── */
.loop-box {
    background: rgba(26, 35, 50, 0.6);
    border-left: 3px solid #6cc0e0;
    border-radius: 0 6px 6px 0;
    padding: 18px 24px;
    line-height: 1.8;
    color: #a8c4d8;
    font-size: 14px;
}
.loop-box strong { color: #e8eef4; font-weight: 500; }

/* ── Explainer (sub-pages) ── */
.explainer {
    background: rgba(26, 35, 50, 0.5);
    border-left: 3px solid #3a6888;
    border-radius: 0 6px 6px 0;
    padding: 14px 18px;
    color: #a0bfd2;
    font-size: 13px;
    line-height: 1.7;
    height: 100%;
}
.explainer strong { color: #e8eef4; font-weight: 500; }

/* ── Metric card (pages 2 + 3) ── */
.metric-card {
    background: rgba(26, 35, 50, 0.7);
    border: 1px solid #3a6888;
    border-radius: 8px;
    padding: 16px;
    text-align: center;
}
.metric-val {
    font-family: 'DM Serif Display', serif;
    font-size: 28px;
    color: #6cc0e0;
}
.metric-val.positive { color: #4caf7d; }
.metric-val.negative { color: #e05050; }
.metric-lbl {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: #7098b0;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-top: 4px;
}
.metric-note { font-size: 11px; color: #506070; margin-top: 2px; }

/* ── Signal header (page 1) ── */
.signal-header {
    background: rgba(26, 35, 50, 0.7);
    border: 1px solid #3a6888;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 24px;
}
.signal-header.bullish { border-color: #4caf7d; }
.signal-header.bearish { border-color: #e05050; }
.signal-header.neutral { border-color: #7098b0; }
.direction {
    font-family: 'DM Mono', monospace;
    font-size: 20px;
    font-weight: 500;
}
.direction.bullish { color: #4caf7d; }
.direction.bearish { color: #e05050; }
.direction.neutral { color: #a8c4d8; }

/* ── Fusion math (page 1) ── */
.fusion-math {
    font-family: 'DM Mono', monospace;
    font-size: 13px;
    color: #6cc0e0;
    background: rgba(26, 35, 50, 0.8);
    padding: 12px 16px;
    border-radius: 6px;
    margin: 8px 0;
    line-height: 2;
}

/* ── Config + stage boxes (page 4) ── */
.config-box {
    background: rgba(26, 35, 50, 0.7);
    border: 1px solid #3a6888;
    border-radius: 8px;
    padding: 20px 24px;
}
.config-param { font-size: 14px; margin-bottom: 10px; color: #e8eef4; }
.config-param code {
    font-family: 'DM Mono', monospace;
    background: rgba(108, 192, 224, 0.15);
    color: #6cc0e0;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 13px;
}
.config-label { color: #a0bfd2; }
.stage-box {
    background: rgba(26, 35, 50, 0.5);
    border: 1px solid #2a3a4a;
    border-radius: 6px;
    padding: 14px 16px;
    height: 100%;
}
.stage-num {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    font-weight: 500;
    color: #6cc0e0;
    letter-spacing: 0.16em;
    text-transform: uppercase;
}
.stage-title {
    font-family: 'DM Serif Display', serif;
    font-size: 17px;
    color: #e8eef4;
    margin: 6px 0;
}
.stage-desc {
    font-size: 12px;
    color: #a0bfd2;
    line-height: 1.6;
}
.best-badge {
    display: inline-block;
    background: rgba(76, 175, 125, 0.2);
    border: 1px solid #4caf7d;
    color: #4caf7d;
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 2px 8px;
    border-radius: 4px;
    margin-left: 8px;
}
</style>
"""
