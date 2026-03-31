"""Tests for data_loader — synthetic fallback and DataFrame conversion."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.data_loader import (
    _synthetic_backtest_result,
    _synthetic_signals,
    load_backtest_result,
    load_latest_signals,
    signals_to_dataframe,
)


def test_synthetic_signals_structure():
    signals = _synthetic_signals()
    assert len(signals) == 3
    for s in signals:
        assert "pair" in s
        assert "signal" in s
        assert "confidence" in s
        assert "technical_score" in s
        assert "sentiment_score" in s
        assert set(s["indicators"]) == {"ema_crossover", "rsi", "macd", "bollinger"}


def test_synthetic_signals_fusion():
    signals = _synthetic_signals()
    for s in signals:
        expected = round(0.6 * s["technical_score"] + 0.4 * s["sentiment_score"], 4)
        assert abs(s["signal"] - expected) < 1e-3


def test_synthetic_signals_seeded():
    a = _synthetic_signals()
    b = _synthetic_signals()
    assert a[0]["signal"] == b[0]["signal"]


def test_signals_to_dataframe_columns():
    signals = _synthetic_signals()
    df = signals_to_dataframe(signals)
    assert len(df) == 3
    for col in ["pair", "signal", "confidence", "technical", "sentiment", "ema", "rsi", "macd", "bollinger"]:
        assert col in df.columns


def test_load_latest_signals_fallback_when_no_dir():
    signals = load_latest_signals(signals_dir=Path("/nonexistent/path"))
    assert isinstance(signals, list)
    assert len(signals) > 0


def test_synthetic_backtest_result_structure():
    result = _synthetic_backtest_result()
    assert "pair" in result
    assert "metrics" in result
    assert "trades" in result
    assert "equity_curve" in result
    expected_metrics = {"total_return_pct", "sharpe_ratio", "sortino_ratio",
                        "max_drawdown_pct", "win_rate", "profit_factor", "total_trades"}
    assert expected_metrics == set(result["metrics"])


def test_synthetic_backtest_equity_curve_positive():
    result = _synthetic_backtest_result()
    assert all(e > 0 for e in result["equity_curve"])


def test_load_backtest_result_fallback():
    result = load_backtest_result(result_path=Path("/nonexistent/result.json"))
    assert "metrics" in result
    assert result["metrics"]["total_trades"] > 0
