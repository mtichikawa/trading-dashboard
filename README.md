# trading-dashboard · T5

Streamlit multi-page oversight dashboard for the T1–T5 paper trading arc. Reads signal output from T3 and backtest results from T4. Falls back to synthetic data when live files are unavailable — no database or paid APIs required to run.

**[Live Demo](https://mtichikawa-trading.streamlit.app)**

---

## Trading Arc

| Repo | Role | Status |
|------|------|--------|
| T1 · crypto-data-pipeline | Live OHLCV ingestion · market event tagging | Shipped Mar 6 |
| T2 · trading-chart-generator | Candlestick PNGs + JSON sidecars · 25/25 tests | Shipped Mar 10 |
| T3 · trading-signal-engine | Technical indicators + FinBERT sentiment · 51/51 tests | Shipped Mar 16 |
| T4 · trading-backtester | Backtesting + parameter sweep · 72/72 tests | Shipped Mar 26 |
| **T5 · trading-dashboard** | Streamlit oversight UI · 8/8 tests | Shipped Mar 31 |

---

## Pages

| Page | What It Shows |
|------|---------------|
| **Home** | Arc overview, pipeline flow (T1→T5), feedback loop explanation |
| **Signal Pipeline** | How T1–T3 generate a signal: indicator breakdown, fusion math, per-pair output |
| **Backtesting** | T4 equity curve, performance metrics, trade log, P&L distribution |
| **Performance** | Equity + drawdown subplot, risk metrics, win/loss breakdown |
| **Parameters** | Sweep results table, current config, T3↔T4 feedback loop detail |

---

## Architecture

```
T3 signals/          T4 results/
     │                    │
     ▼                    ▼
src/data_loader.py  ──────────────── synthetic fallback
     │
     ├── load_latest_signals()      → Signal Pipeline page
     ├── load_backtest_result()     → Backtesting / Performance / Parameters pages
     └── synthetic_sweep_results() → Parameters page

src/charts.py
     ├── indicator_bar_chart()     → per-indicator Plotly horizontal bar chart
     ├── equity_curve_chart()      → Plotly equity line with fill
     ├── equity_with_drawdown()    → two-panel subplot (equity + drawdown %)
     └── pnl_histogram()           → trade P&L distribution histogram
```

---

## Setup

```bash
cd trading-dashboard
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
# Launch Streamlit dashboard
streamlit run app.py

# Quick demo — no database or signal files needed
python examples/quick_demo.py
```

## Tests

```bash
pytest tests/ -v
# 8/8 — data_loader synthetic fallback and DataFrame conversion
```

---

## Connecting to Live Arc Data

By default the dashboard uses synthetic data. To connect to live T3/T4 output:

- **Signals**: point `SIGNALS_DIR` in `src/data_loader.py` to your local `trading-signal-engine/signals/` directory
- **Backtest results**: pass a path to `load_backtest_result()` pointing to a T4 result JSON

The data shapes are identical between synthetic and live data — no page code changes required.

---

## Contact

Mike Ichikawa · [projects.ichikawa@gmail.com](mailto:projects.ichikawa@gmail.com) · [mtichikawa.github.io](https://mtichikawa.github.io)
