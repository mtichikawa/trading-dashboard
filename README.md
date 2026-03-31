# trading-dashboard · T5

Streamlit multi-page oversight dashboard for the T1–T5 trading arc. Reads signal output from [trading-signal-engine (T3)](../trading-signal-engine) and backtest results from [trading-backtester (T4)](../trading-backtester). Falls back to synthetic data when live files are unavailable — no database or paid APIs required to run.

## Pages

| Page | Description |
|------|-------------|
| Home | Arc overview and navigation |
| Live Signals | Latest T3 signal per pair/timeframe with indicator breakdown |
| Portfolio | Trade summary and active parameter configuration |
| Performance | Equity curve, Sharpe, Sortino, drawdown |
| Parameters | T4 sweep results and T3 weight review |

## Setup

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
# Launch dashboard
streamlit run app.py

# Quick demo (no DB or signal files needed)
python examples/quick_demo.py
```

## Tests

```bash
pytest tests/ -v
```

## Trading Arc

| Repo | Role |
|------|------|
| [crypto-data-pipeline](../crypto-data-pipeline) | T1 — Live OHLCV via ccxt/Kraken |
| [trading-chart-generator](../trading-chart-generator) | T2 — Candlestick PNGs + JSON sidecars |
| [trading-signal-engine](../trading-signal-engine) | T3 — Technical + FinBERT sentiment signals |
| [trading-backtester](../trading-backtester) | T4 — Backtesting + parameter sweep |
| trading-dashboard | T5 — This app |
