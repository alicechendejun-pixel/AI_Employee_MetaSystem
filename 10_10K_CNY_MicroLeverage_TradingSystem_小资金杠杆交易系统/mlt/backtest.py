from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .models import Bar, ContractSpec, RiskConfig, StrategyConfig, Trade
from .risk import drawdown_exceeded, size_order
from .strategy import signal_at


@dataclass
class OpenPosition:
    side: str
    qty: int
    entry_date: str
    entry_price: float
    stop: float
    take_profit: float | None


def run_backtest(
    bars: list[Bar],
    symbol: str,
    contract: ContractSpec,
    risk: RiskConfig,
    strategy: StrategyConfig,
) -> dict[str, Any]:
    if len(bars) < max(strategy.entry_lookback, strategy.atr_period, strategy.trend_sma_period) + 2:
        raise ValueError("Not enough bars for configured strategy")

    equity = risk.capital
    peak_equity = equity
    position: OpenPosition | None = None
    trades: list[Trade] = []
    equity_curve: list[dict[str, float | str]] = []

    start = max(strategy.entry_lookback, strategy.atr_period, strategy.trend_sma_period)
    i = start
    while i < len(bars):
        bar = bars[i]

        if position is not None:
            exit_price, exit_reason = _exit_price(position, bar, contract, risk)
            if exit_price is not None:
                trade = _close_trade(symbol, position, bar.date, exit_price, contract, risk, exit_reason)
                trades.append(trade)
                equity += trade.net_pnl
                peak_equity = max(peak_equity, equity)
                position = None
                equity_curve.append({"date": bar.date, "equity": round(equity, 6)})
                if drawdown_exceeded(peak_equity, equity, risk):
                    break
                i += 1
                continue

        if position is None and i < len(bars) - 1:
            signal = signal_at(bars, i, symbol, strategy)
            sizing = size_order(signal, contract, risk, equity=equity)
            if sizing.accepted and signal.stop is not None:
                next_bar = bars[i + 1]
                entry_price = _entry_fill(signal.side, next_bar.open, contract, risk)
                # Keep the original signal stop. If entry gaps beyond stop, reject.
                if signal.side == "LONG" and entry_price > signal.stop:
                    position = OpenPosition(
                        side=signal.side,
                        qty=sizing.qty,
                        entry_date=next_bar.date,
                        entry_price=entry_price,
                        stop=signal.stop,
                        take_profit=signal.take_profit,
                    )
                elif signal.side == "SHORT" and entry_price < signal.stop:
                    position = OpenPosition(
                        side=signal.side,
                        qty=sizing.qty,
                        entry_date=next_bar.date,
                        entry_price=entry_price,
                        stop=signal.stop,
                        take_profit=signal.take_profit,
                    )
                i += 1
                continue

        equity_curve.append({"date": bar.date, "equity": round(equity, 6)})
        i += 1

    if position is not None:
        last = bars[-1]
        exit_price = _exit_fill(position.side, last.close, contract, risk)
        trade = _close_trade(symbol, position, last.date, exit_price, contract, risk, "end_of_data")
        trades.append(trade)
        equity += trade.net_pnl
        equity_curve.append({"date": last.date, "equity": round(equity, 6)})

    return _metrics(risk.capital, equity, trades, equity_curve)


def _entry_fill(side: str, price: float, contract: ContractSpec, risk: RiskConfig) -> float:
    slip = risk.slippage_ticks * contract.tick_size
    return price + slip if side == "LONG" else price - slip


def _exit_fill(side: str, price: float, contract: ContractSpec, risk: RiskConfig) -> float:
    slip = risk.slippage_ticks * contract.tick_size
    return price - slip if side == "LONG" else price + slip


def _exit_price(
    position: OpenPosition,
    bar: Bar,
    contract: ContractSpec,
    risk: RiskConfig,
) -> tuple[float | None, str]:
    if position.side == "LONG":
        if bar.low <= position.stop:
            return _exit_fill(position.side, position.stop, contract, risk), "stop"
        if position.take_profit is not None and bar.high >= position.take_profit:
            return _exit_fill(position.side, position.take_profit, contract, risk), "take_profit"
    else:
        if bar.high >= position.stop:
            return _exit_fill(position.side, position.stop, contract, risk), "stop"
        if position.take_profit is not None and bar.low <= position.take_profit:
            return _exit_fill(position.side, position.take_profit, contract, risk), "take_profit"
    return None, ""


def _close_trade(
    symbol: str,
    position: OpenPosition,
    exit_date: str,
    exit_price: float,
    contract: ContractSpec,
    risk: RiskConfig,
    exit_reason: str,
) -> Trade:
    direction = 1.0 if position.side == "LONG" else -1.0
    gross = (exit_price - position.entry_price) * direction * position.qty * contract.multiplier
    fees = 2.0 * risk.commission_per_contract * position.qty
    return Trade(
        symbol=symbol,
        side=position.side,
        qty=position.qty,
        entry_date=position.entry_date,
        entry_price=round(position.entry_price, 6),
        exit_date=exit_date,
        exit_price=round(exit_price, 6),
        gross_pnl=round(gross, 6),
        fees=round(fees, 6),
        net_pnl=round(gross - fees, 6),
        exit_reason=exit_reason,
    )


def _metrics(
    starting_equity: float,
    ending_equity: float,
    trades: list[Trade],
    equity_curve: list[dict[str, float | str]],
) -> dict[str, Any]:
    wins = [t for t in trades if t.net_pnl > 0]
    losses = [t for t in trades if t.net_pnl <= 0]
    gross_profit = sum(t.net_pnl for t in wins)
    gross_loss = abs(sum(t.net_pnl for t in losses))
    profit_factor = gross_profit / gross_loss if gross_loss else None
    max_drawdown = _max_drawdown([float(point["equity"]) for point in equity_curve])
    return {
        "starting_equity": round(starting_equity, 6),
        "ending_equity": round(ending_equity, 6),
        "net_pnl": round(ending_equity - starting_equity, 6),
        "return_fraction": round((ending_equity - starting_equity) / starting_equity, 6),
        "trade_count": len(trades),
        "win_rate": round(len(wins) / len(trades), 6) if trades else None,
        "profit_factor": round(profit_factor, 6) if profit_factor is not None else None,
        "max_drawdown_fraction": round(max_drawdown, 6),
        "trades": [t.__dict__ for t in trades],
        "equity_curve": equity_curve,
    }


def _max_drawdown(equity_values: list[float]) -> float:
    if not equity_values:
        return 0.0
    peak = equity_values[0]
    max_dd = 0.0
    for value in equity_values:
        peak = max(peak, value)
        if peak:
            max_dd = max(max_dd, (peak - value) / peak)
    return max_dd

