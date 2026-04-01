"""Quick demo — runs without a database, T3 signal files, or any paid APIs.

Prints synthetic signal and backtest data to stdout to verify the full
data pipeline works end-to-end. Same data shown in the Streamlit dashboard.

Usage:
    python examples/quick_demo.py

Then launch the dashboard:
    streamlit run app.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.data_loader import (
    load_backtest_result,
    load_latest_signals,
    signals_to_dataframe,
    synthetic_sweep_results,
)

SEPARATOR = "─" * 56


def main():
    print("\n=== Trading Arc Dashboard — Quick Demo ===")
    print("    T1–T5 paper trading system · synthetic data mode\n")

    # Signals
    print(SEPARATOR)
    print("  SIGNALS  (T3 — trading-signal-engine)")
    print(SEPARATOR)
    signals = load_latest_signals()
    df = signals_to_dataframe(signals)
    for _, row in df.iterrows():
        sig = row["signal"]
        direction = "BUY " if sig > 0.1 else "SELL" if sig < -0.1 else "HOLD"
        print(
            f"  {row['pair']:10s} {row['timeframe']:4s}  "
            f"{direction}  signal={sig:+.4f}  conf={row['confidence']:.2f}  "
            f"tech={row['technical']:+.3f}  sent={row['sentiment']:+.3f}"
        )
    print()

    # Backtest
    print(SEPARATOR)
    print("  BACKTEST  (T4 — trading-backtester)")
    print(SEPARATOR)
    result = load_backtest_result()
    m = result["metrics"]
    p = result["parameters"]
    print(f"  Pair:           {result['pair']} {result['timeframe']}")
    print(f"  Tech weight:    {p['tech_weight']}  |  Sent weight: {p['sent_weight']}")
    print(f"  Threshold:      |signal| > {p['signal_threshold']}  |  Stop loss: {p['stop_loss_pct']:.0%}")
    print()
    print(f"  Total return:   {m['total_return_pct']:+.2f}%")
    print(f"  Sharpe ratio:   {m['sharpe_ratio']:.2f}")
    print(f"  Sortino ratio:  {m['sortino_ratio']:.2f}")
    print(f"  Max drawdown:   {m['max_drawdown_pct']:.2f}%")
    print(f"  Win rate:       {m['win_rate']:.1%}  ({m['total_trades']} trades)")
    print(f"  Profit factor:  {m['profit_factor']:.2f}")
    print()

    # Sweep
    print(SEPARATOR)
    print("  PARAMETER SWEEP  (top 5 configs by Sharpe)")
    print(SEPARATOR)
    sweep = synthetic_sweep_results().head(5)
    print(f"  {'tech':>5}  {'sent':>5}  {'thresh':>7}  {'sl':>5}  {'sharpe':>7}  {'return':>8}  {'winrate':>8}")
    for _, row in sweep.iterrows():
        print(
            f"  {row['tech_weight']:>5.1f}  {row['sent_weight']:>5.1f}  "
            f"{row['signal_threshold']:>7.2f}  {row['stop_loss']:>5}  "
            f"{row['sharpe']:>7.2f}  {row['return_pct']:>8}  {row['win_rate']:>8}"
        )
    print()

    print(SEPARATOR)
    print("  Launch the dashboard:")
    print("    streamlit run app.py")
    print(SEPARATOR)
    print()


if __name__ == "__main__":
    main()
