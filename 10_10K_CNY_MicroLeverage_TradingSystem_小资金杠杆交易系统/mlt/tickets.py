from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import ContractSpec, OrderSizing, RiskConfig, Signal


def build_ticket(
    signal: Signal,
    sizing: OrderSizing,
    contract: ContractSpec,
    risk: RiskConfig,
) -> dict[str, Any]:
    action = "BUY" if signal.side == "LONG" else "SELL" if signal.side == "SHORT" else "NONE"
    exit_action = "SELL" if signal.side == "LONG" else "BUY" if signal.side == "SHORT" else "NONE"
    return {
        "status": "READY" if sizing.accepted else "REJECTED",
        "reject_reason": None if sizing.accepted else sizing.reason,
        "symbol": signal.symbol,
        "signal_date": signal.date,
        "side": signal.side,
        "entry_reference": signal.entry,
        "stop": signal.stop,
        "take_profit": signal.take_profit,
        "qty": sizing.qty,
        "parent_order": {
            "action": action,
            "order_type": "LIMIT_OR_MARKET_AFTER_REVIEW",
            "qty": sizing.qty,
            "reference_price": signal.entry,
        },
        "protective_stop": {
            "action": exit_action,
            "order_type": "STOP",
            "qty": sizing.qty,
            "stop_price": signal.stop,
        },
        "take_profit_order": {
            "action": exit_action,
            "order_type": "LIMIT",
            "qty": sizing.qty,
            "limit_price": signal.take_profit,
        },
        "risk": {
            "capital": risk.capital,
            "risk_budget": sizing.risk_budget,
            "risk_per_contract": sizing.risk_per_contract,
            "margin_per_contract": sizing.margin_per_contract,
            "margin_required": sizing.margin_required,
            "max_margin_fraction": risk.max_margin_fraction,
        },
        "contract": {
            "multiplier": contract.multiplier,
            "tick_size": contract.tick_size,
            "margin_rate": contract.margin_rate,
            "min_qty": contract.min_qty,
            "lot_step": contract.lot_step,
            "currency": contract.currency,
            "description": contract.description,
        },
        "review_checklist": [
            "Broker contract symbol exactly matches this ticket.",
            "Multiplier, tick size, commission, and margin match broker screen.",
            "Stop order is entered at the same time as the entry order.",
            "No trade is placed if daily loss or drawdown kill switch is active.",
            "No trade is placed during limit-up/limit-down, illiquid, or abnormal spread conditions.",
        ],
        "reason": signal.reason,
    }


def write_ticket(ticket: dict[str, Any], outdir: str | Path) -> tuple[Path, Path]:
    target = Path(outdir)
    target.mkdir(parents=True, exist_ok=True)
    json_path = target / "latest_ticket.json"
    md_path = target / "latest_ticket.md"
    json_path.write_text(json.dumps(ticket, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(_ticket_markdown(ticket), encoding="utf-8")
    return json_path, md_path


def _ticket_markdown(ticket: dict[str, Any]) -> str:
    lines = [
        "# Manual Order Ticket",
        "",
        f"Status: {ticket['status']}",
        f"Symbol: {ticket['symbol']}",
        f"Signal date: {ticket['signal_date']}",
        f"Side: {ticket['side']}",
        f"Quantity: {ticket['qty']}",
        f"Entry reference: {ticket['entry_reference']}",
        f"Stop: {ticket['stop']}",
        f"Take profit: {ticket['take_profit']}",
        "",
        "## Risk",
        f"Capital: {ticket['risk']['capital']}",
        f"Risk budget: {ticket['risk']['risk_budget']}",
        f"Risk per contract: {ticket['risk']['risk_per_contract']}",
        f"Margin required: {ticket['risk']['margin_required']}",
        "",
        "## Checklist",
    ]
    lines.extend(f"- {item}" for item in ticket["review_checklist"])
    if ticket["status"] == "REJECTED":
        lines.extend(["", f"Reject reason: {ticket['reject_reason']}"])
    lines.extend(["", f"Reason: {ticket['reason']}", ""])
    return "\n".join(lines)
