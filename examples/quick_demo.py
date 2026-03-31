"""Quick demo — runs without a database, T3 signal files, or any paid APIs.

Prints synthetic signal and backtest data to stdout to verify the
data_loader module works end-to-end.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.data_loader import (
    _synthetic_backtest_result,
    load_latest_signals,
    signals_to_dataframe,
)


def main():
    print("=== Trading Dashboard — Quick Demo ===\n")

    print("--- Signals (T3 output) ---")
    signals = load_latest_signals()
    df = signals_to_dataframe(signals)
    print(df[["pair", "timeframe", "signal", "confidence", "technical", "sentiment"]].to_string(index=False))
    print()

    print("--- Backtest Result (T4 output) ---")
    result = _synthetic_backtest_result()
    m = result["metrics"]
    print(f"Pair:          {result['pair']} {result['timeframe']}")
    print(f"Total return:  {m['total_return_pct']:+.2f}%")
    print(f"Sharpe:        {m['sharpe_ratio']:.2f}")
    print(f"Sortino:       {m['sortino_ratio']:.2f}")
    print(f"Max drawdown:  {m['max_drawdown_pct']:.2f}%")
    print(f"Win rate:      {m['win_rate']:.1%}")
    print(f"Total trades:  {m['total_trades']}")
    print()

    print("Done. Run `streamlit run app.py` to launch the dashboard.")


if __name__ == "__main__":
    main()
