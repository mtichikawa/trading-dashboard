"""Data loading utilities for the trading dashboard.

Reads T3 signal JSON files and T4 backtest results.
Falls back to synthetic data when live files are unavailable.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

# Paths relative to this repo's position in the arc
_ROOT = Path(__file__).parent.parent.parent
SIGNALS_DIR = _ROOT / "trading-signal-engine" / "signals"
BACKTESTER_DIR = _ROOT / "trading-backtester"


def load_latest_signals(signals_dir: Path = SIGNALS_DIR) -> List[Dict]:
    """Load the most recent T3 signal JSON.

    Returns a list of signal dicts, one per pair/timeframe.
    Falls back to synthetic data if the signals directory is missing.
    """
    signals_dir = Path(signals_dir)
    if not signals_dir.exists():
        return _synthetic_signals()

    files = sorted(signals_dir.glob("signals_*.json"))
    if not files:
        return _synthetic_signals()

    with open(files[-1]) as f:
        data = json.load(f)

    return data.get("signals", _synthetic_signals())


def signals_to_dataframe(signals: List[Dict]) -> pd.DataFrame:
    """Flatten signal list to a DataFrame for display."""
    rows = []
    for s in signals:
        rows.append({
            "pair": s["pair"],
            "timeframe": s["timeframe"],
            "signal": s["signal"],
            "confidence": s["confidence"],
            "technical": s["technical_score"],
            "sentiment": s["sentiment_score"],
            "ema": s["indicators"]["ema_crossover"],
            "rsi": s["indicators"]["rsi"],
            "macd": s["indicators"]["macd"],
            "bollinger": s["indicators"]["bollinger"],
            "timestamp": s["timestamp"],
        })
    return pd.DataFrame(rows)


def load_backtest_result(result_path: Optional[Path] = None) -> Dict:
    """Load a T4 backtest result JSON.

    Falls back to synthetic result if path is not provided or file is missing.
    """
    if result_path is not None and Path(result_path).exists():
        with open(result_path) as f:
            return json.load(f)
    return _synthetic_backtest_result()


def _synthetic_signals() -> List[Dict]:
    """Synthetic signals matching T3 output format, seeded for reproducibility."""
    rng = np.random.default_rng(42)
    now = datetime.utcnow().isoformat() + "+00:00"
    pairs = [("BTC/USD", "1h"), ("ETH/USD", "4h"), ("SOL/USD", "1h")]
    signals = []
    for pair, timeframe in pairs:
        tech = float(rng.uniform(-0.5, 0.5))
        sent = float(rng.uniform(-0.3, 0.7))
        signal = round(0.6 * tech + 0.4 * sent, 4)
        confidence = round(max(0.0, 1.0 - abs(tech - sent)), 4)
        signals.append({
            "pair": pair,
            "timeframe": timeframe,
            "timestamp": now,
            "signal": signal,
            "confidence": confidence,
            "technical_score": round(tech, 4),
            "sentiment_score": round(sent, 4),
            "indicators": {
                "ema_crossover": round(float(rng.uniform(-0.3, 0.3)), 4),
                "rsi": round(float(rng.uniform(-0.5, 0.5)), 4),
                "macd": round(float(rng.uniform(-1.0, 1.0)), 4),
                "bollinger": round(float(rng.uniform(-0.5, 0.5)), 4),
            },
            "headlines_used": [],
            "chart_path": f"charts/{pair.replace('/', '_')}_{timeframe}.png",
        })
    return signals


def _synthetic_backtest_result() -> Dict:
    """Synthetic backtest result matching T4 output format."""
    rng = np.random.default_rng(99)
    n = 200
    returns = rng.normal(0.0002, 0.008, n)
    equity = [10000.0]
    for r in returns:
        equity.append(equity[-1] * (1 + r))

    trades = []
    for i in range(0, n - 5, 8):
        pnl = float(rng.normal(0.003, 0.015))
        trades.append({
            "entry_price": round(equity[i], 2),
            "exit_price": round(equity[i] * (1 + pnl), 2),
            "side": "long" if rng.random() > 0.35 else "short",
            "pnl_pct": round(pnl, 6),
            "bars_held": int(rng.integers(2, 12)),
        })

    wins = [t for t in trades if t["pnl_pct"] > 0]
    total_return = (equity[-1] - equity[0]) / equity[0] * 100

    return {
        "pair": "BTC/USD",
        "timeframe": "1h",
        "parameters": {
            "signal_threshold": 0.1,
            "stop_loss_pct": 0.02,
            "tech_weight": 0.6,
            "sent_weight": 0.4,
        },
        "metrics": {
            "total_return_pct": round(total_return, 4),
            "sharpe_ratio": 1.42,
            "sortino_ratio": 2.07,
            "max_drawdown_pct": 8.3,
            "win_rate": round(len(wins) / len(trades), 4) if trades else 0.0,
            "profit_factor": 1.65,
            "total_trades": len(trades),
        },
        "trades": trades,
        "equity_curve": [round(e, 2) for e in equity],
    }
