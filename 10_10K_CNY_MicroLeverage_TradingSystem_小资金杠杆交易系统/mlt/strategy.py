from __future__ import annotations

from .indicators import atr, previous_high, previous_low, sma
from .models import Bar, Signal, StrategyConfig


def latest_signal(bars: list[Bar], symbol: str, config: StrategyConfig) -> Signal:
    if not bars:
        raise ValueError("bars cannot be empty")
    index = len(bars) - 1
    return signal_at(bars, index, symbol, config)


def signal_at(bars: list[Bar], index: int, symbol: str, config: StrategyConfig) -> Signal:
    if index < 0 or index >= len(bars):
        raise IndexError("index out of range")

    bar = bars[index]
    min_index = max(config.entry_lookback, config.atr_period, config.trend_sma_period) - 1
    if index < min_index:
        return Signal(symbol, bar.date, "FLAT", bar.close, None, None, "not_enough_history")

    highs = previous_high(bars, index, config.entry_lookback)
    lows = previous_low(bars, index, config.entry_lookback)
    atr_values = atr(bars[: index + 1], config.atr_period)
    trend_values = sma([b.close for b in bars[: index + 1]], config.trend_sma_period)
    current_atr = atr_values[-1]
    trend = trend_values[-1]

    if highs is None or lows is None or current_atr is None or trend is None:
        return Signal(symbol, bar.date, "FLAT", bar.close, None, None, "indicator_not_ready")

    if bar.close > highs and bar.close > trend:
        stop = bar.close - config.atr_stop_multiple * current_atr
        risk = bar.close - stop
        take_profit = bar.close + config.take_profit_r_multiple * risk
        return Signal(
            symbol=symbol,
            date=bar.date,
            side="LONG",
            entry=bar.close,
            stop=round(stop, 6),
            take_profit=round(take_profit, 6),
            reason=f"close {bar.close:.4f} broke previous {config.entry_lookback}-bar high {highs:.4f}",
        )

    if bar.close < lows and bar.close < trend:
        stop = bar.close + config.atr_stop_multiple * current_atr
        risk = stop - bar.close
        take_profit = bar.close - config.take_profit_r_multiple * risk
        return Signal(
            symbol=symbol,
            date=bar.date,
            side="SHORT",
            entry=bar.close,
            stop=round(stop, 6),
            take_profit=round(take_profit, 6),
            reason=f"close {bar.close:.4f} broke previous {config.entry_lookback}-bar low {lows:.4f}",
        )

    return Signal(symbol, bar.date, "FLAT", bar.close, None, None, "no_breakout")

