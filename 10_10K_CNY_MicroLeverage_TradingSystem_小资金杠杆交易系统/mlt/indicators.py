from __future__ import annotations

from .models import Bar


def sma(values: list[float], period: int) -> list[float | None]:
    if period <= 0:
        raise ValueError("period must be positive")
    out: list[float | None] = []
    running = 0.0
    for i, value in enumerate(values):
        running += value
        if i >= period:
            running -= values[i - period]
        out.append(running / period if i >= period - 1 else None)
    return out


def atr(bars: list[Bar], period: int) -> list[float | None]:
    if period <= 0:
        raise ValueError("period must be positive")
    true_ranges: list[float] = []
    for i, bar in enumerate(bars):
        if i == 0:
            true_ranges.append(bar.high - bar.low)
            continue
        prev_close = bars[i - 1].close
        true_ranges.append(
            max(
                bar.high - bar.low,
                abs(bar.high - prev_close),
                abs(bar.low - prev_close),
            )
        )
    return sma(true_ranges, period)


def previous_high(bars: list[Bar], index: int, lookback: int) -> float | None:
    if lookback <= 0:
        raise ValueError("lookback must be positive")
    if index < lookback:
        return None
    return max(bar.high for bar in bars[index - lookback:index])


def previous_low(bars: list[Bar], index: int, lookback: int) -> float | None:
    if lookback <= 0:
        raise ValueError("lookback must be positive")
    if index < lookback:
        return None
    return min(bar.low for bar in bars[index - lookback:index])

