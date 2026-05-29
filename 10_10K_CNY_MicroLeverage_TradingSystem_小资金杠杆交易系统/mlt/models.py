from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Bar:
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: float = 0.0


@dataclass(frozen=True)
class ContractSpec:
    symbol: str
    multiplier: float
    tick_size: float
    margin_rate: float
    min_qty: int = 1
    lot_step: int = 1
    currency: str = "CNY"
    description: str = ""


@dataclass(frozen=True)
class StrategyConfig:
    entry_lookback: int = 20
    exit_lookback: int = 10
    atr_period: int = 14
    atr_stop_multiple: float = 2.0
    trend_sma_period: int = 50
    take_profit_r_multiple: float = 2.0


@dataclass(frozen=True)
class RiskConfig:
    capital: float = 10000.0
    risk_per_trade_fraction: float = 0.005
    max_margin_fraction: float = 0.35
    max_daily_loss_fraction: float = 0.015
    max_total_drawdown_fraction: float = 0.08
    commission_per_contract: float = 0.0
    slippage_ticks: float = 1.0
    allow_short: bool = True


@dataclass(frozen=True)
class AccountState:
    current_equity: float
    peak_equity: float
    realized_pnl_today: float = 0.0
    open_margin: float = 0.0


@dataclass(frozen=True)
class Signal:
    symbol: str
    date: str
    side: str
    entry: float
    stop: Optional[float]
    take_profit: Optional[float]
    reason: str


@dataclass(frozen=True)
class OrderSizing:
    accepted: bool
    qty: int
    reason: str
    risk_budget: float
    risk_per_contract: float
    margin_per_contract: float
    margin_required: float


@dataclass(frozen=True)
class Trade:
    symbol: str
    side: str
    qty: int
    entry_date: str
    entry_price: float
    exit_date: str
    exit_price: float
    gross_pnl: float
    fees: float
    net_pnl: float
    exit_reason: str
