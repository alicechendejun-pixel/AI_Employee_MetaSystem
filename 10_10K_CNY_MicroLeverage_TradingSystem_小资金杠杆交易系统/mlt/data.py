from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from .models import AccountState, Bar, ContractSpec, RiskConfig, StrategyConfig


def load_bars_csv(path: str | Path) -> list[Bar]:
    rows: list[Bar] = []
    with Path(path).open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        required = {"date", "open", "high", "low", "close"}
        lower_names = {name.lower(): name for name in reader.fieldnames or []}
        missing = required - set(lower_names)
        if missing:
            raise ValueError(f"Missing CSV columns: {sorted(missing)}")

        for raw in reader:
            row = {k.lower(): raw[v] for k, v in lower_names.items()}
            rows.append(
                Bar(
                    date=row["date"],
                    open=float(row["open"]),
                    high=float(row["high"]),
                    low=float(row["low"]),
                    close=float(row["close"]),
                    volume=float(row.get("volume") or 0.0),
                )
            )

    if len(rows) < 3:
        raise ValueError("Need at least 3 bars")
    for bar in rows:
        if bar.high < max(bar.open, bar.close, bar.low):
            raise ValueError(f"Invalid high/low relationship at {bar.date}")
        if bar.low > min(bar.open, bar.close, bar.high):
            raise ValueError(f"Invalid high/low relationship at {bar.date}")
    return rows


def load_json(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as f:
        return json.load(f)


def load_contract(path: str | Path, symbol: str) -> ContractSpec:
    payload = load_json(path)
    if symbol not in payload:
        raise KeyError(f"Contract spec not found for symbol {symbol}")
    raw = payload[symbol]
    return ContractSpec(
        symbol=raw.get("symbol", symbol),
        multiplier=float(raw["multiplier"]),
        tick_size=float(raw["tick_size"]),
        margin_rate=float(raw["margin_rate"]),
        min_qty=int(raw.get("min_qty", 1)),
        lot_step=int(raw.get("lot_step", raw.get("min_qty", 1))),
        currency=raw.get("currency", "CNY"),
        description=raw.get("description", ""),
    )


def load_configs(path: str | Path) -> tuple[RiskConfig, StrategyConfig, dict[str, Any]]:
    payload = load_json(path)
    account = payload.get("account", {})
    risk = payload.get("risk", {})
    strategy = payload.get("strategy", {})
    return (
        RiskConfig(
            capital=float(account.get("capital", 10000.0)),
            risk_per_trade_fraction=float(risk.get("risk_per_trade_fraction", 0.005)),
            max_margin_fraction=float(risk.get("max_margin_fraction", 0.35)),
            max_daily_loss_fraction=float(risk.get("max_daily_loss_fraction", 0.015)),
            max_total_drawdown_fraction=float(risk.get("max_total_drawdown_fraction", 0.08)),
            commission_per_contract=float(risk.get("commission_per_contract", 0.0)),
            slippage_ticks=float(risk.get("slippage_ticks", 1.0)),
            allow_short=bool(risk.get("allow_short", True)),
        ),
        StrategyConfig(
            entry_lookback=int(strategy.get("entry_lookback", 20)),
            exit_lookback=int(strategy.get("exit_lookback", 10)),
            atr_period=int(strategy.get("atr_period", 14)),
            atr_stop_multiple=float(strategy.get("atr_stop_multiple", 2.0)),
            trend_sma_period=int(strategy.get("trend_sma_period", 50)),
            take_profit_r_multiple=float(strategy.get("take_profit_r_multiple", 2.0)),
        ),
        payload,
    )


def load_account_state(path: str | Path, default_capital: float) -> AccountState:
    if not Path(path).exists():
        raise FileNotFoundError(path)
    raw = load_json(path)
    current_equity = float(raw.get("current_equity", default_capital))
    return AccountState(
        current_equity=current_equity,
        peak_equity=float(raw.get("peak_equity", current_equity)),
        realized_pnl_today=float(raw.get("realized_pnl_today", 0.0)),
        open_margin=float(raw.get("open_margin", 0.0)),
    )
