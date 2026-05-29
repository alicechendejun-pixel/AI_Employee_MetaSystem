from __future__ import annotations

import math

from .models import ContractSpec, OrderSizing, RiskConfig, Signal


def size_order(
    signal: Signal,
    contract: ContractSpec,
    risk: RiskConfig,
    equity: float | None = None,
    open_margin: float = 0.0,
) -> OrderSizing:
    account_equity = risk.capital if equity is None else equity
    risk_budget = account_equity * risk.risk_per_trade_fraction
    if signal.side == "FLAT":
        return _reject("flat_signal", risk_budget, 0.0, 0.0)
    if signal.side == "SHORT" and not risk.allow_short:
        return _reject("short_disabled", risk_budget, 0.0, 0.0)
    if signal.stop is None:
        return _reject("missing_stop", risk_budget, 0.0, 0.0)

    stop_distance = abs(signal.entry - signal.stop)
    if stop_distance <= 0:
        return _reject("invalid_stop_distance", risk_budget, 0.0, 0.0)

    slippage_value = risk.slippage_ticks * contract.tick_size * contract.multiplier
    risk_per_contract = (
        stop_distance * contract.multiplier
        + 2.0 * slippage_value
        + 2.0 * risk.commission_per_contract
    )
    if risk_per_contract <= 0:
        return _reject("invalid_contract_risk", risk_budget, 0.0, 0.0)

    qty_by_risk = math.floor(risk_budget / risk_per_contract)

    margin_per_contract = abs(signal.entry) * contract.multiplier * contract.margin_rate
    margin_room = max(0.0, account_equity * risk.max_margin_fraction - open_margin)
    qty_by_margin = math.floor(margin_room / margin_per_contract) if margin_per_contract > 0 else 0

    raw_qty = min(qty_by_risk, qty_by_margin)
    lot_step = max(1, contract.lot_step)
    qty = (raw_qty // lot_step) * lot_step
    if qty < contract.min_qty:
        reason = (
            "risk_budget_too_small"
            if qty_by_risk < contract.min_qty
            else "margin_room_too_small"
        )
        return OrderSizing(
            accepted=False,
            qty=0,
            reason=reason,
            risk_budget=round(risk_budget, 6),
            risk_per_contract=round(risk_per_contract, 6),
            margin_per_contract=round(margin_per_contract, 6),
            margin_required=0.0,
        )

    return OrderSizing(
        accepted=True,
        qty=int(qty),
        reason="accepted",
        risk_budget=round(risk_budget, 6),
        risk_per_contract=round(risk_per_contract, 6),
        margin_per_contract=round(margin_per_contract, 6),
        margin_required=round(qty * margin_per_contract, 6),
    )


def daily_loss_exceeded(realized_loss_today: float, risk: RiskConfig, equity: float | None = None) -> bool:
    account_equity = risk.capital if equity is None else equity
    return realized_loss_today <= -abs(account_equity * risk.max_daily_loss_fraction)


def drawdown_exceeded(peak_equity: float, current_equity: float, risk: RiskConfig) -> bool:
    if peak_equity <= 0:
        return False
    drawdown = (peak_equity - current_equity) / peak_equity
    return drawdown >= risk.max_total_drawdown_fraction


def _reject(reason: str, risk_budget: float, risk_per_contract: float, margin_per_contract: float) -> OrderSizing:
    return OrderSizing(
        accepted=False,
        qty=0,
        reason=reason,
        risk_budget=round(risk_budget, 6),
        risk_per_contract=round(risk_per_contract, 6),
        margin_per_contract=round(margin_per_contract, 6),
        margin_required=0.0,
    )
