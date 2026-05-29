from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .backtest import run_backtest
from .data import load_account_state, load_bars_csv, load_configs, load_contract, load_json
from .models import OrderSizing
from .risk import daily_loss_exceeded, drawdown_exceeded, size_order
from .strategy import latest_signal
from .tickets import build_ticket, write_ticket


def main() -> int:
    parser = argparse.ArgumentParser(prog="mlt", description="Micro Leverage Trader")
    sub = parser.add_subparsers(dest="command", required=True)

    backtest = sub.add_parser("backtest", help="Run a conservative backtest")
    _add_common_args(backtest)

    signal = sub.add_parser("signal", help="Generate latest manual order ticket")
    _add_common_args(signal)

    screen = sub.add_parser("screen", help="Screen a universe and rank tradable candidates")
    screen.add_argument("--universe", required=True, help="Universe JSON path")
    screen.add_argument("--config", default="config.live_guarded_10000_cny.json", help="Config JSON path")
    screen.add_argument("--contracts", default="contracts.example.json", help="Contracts JSON path")
    screen.add_argument("--state", default=None, help="Optional account state JSON for kill switches")
    screen.add_argument("--out", default="runs/screen", help="Output directory")

    args = parser.parse_args()
    risk, strategy, _raw_config = load_configs(args.config)

    if args.command == "screen":
        state = load_account_state(args.state, risk.capital) if args.state else None
        result = screen_universe(args.universe, args.contracts, risk, strategy, state)
        outdir = Path(args.out)
        outdir.mkdir(parents=True, exist_ok=True)
        json_path = outdir / "screen_results.json"
        md_path = outdir / "screen_results.md"
        json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        md_path.write_text(_screen_markdown(result), encoding="utf-8")
        print(json.dumps(result["summary"], ensure_ascii=False, indent=2))
        print(f"Wrote {json_path}")
        print(f"Wrote {md_path}")
        return 0

    bars = load_bars_csv(args.bars)
    contract = load_contract(args.contracts, args.symbol)

    if args.command == "backtest":
        result = run_backtest(bars, args.symbol, contract, risk, strategy)
        outdir = Path(args.out)
        outdir.mkdir(parents=True, exist_ok=True)
        outpath = outdir / "backtest_result.json"
        outpath.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps({k: v for k, v in result.items() if k not in ("trades", "equity_curve")}, indent=2))
        print(f"Wrote {outpath}")
        return 0

    sig = latest_signal(bars, args.symbol, strategy)
    state = load_account_state(args.state, risk.capital) if args.state else None
    sizing = _size_with_kill_switches(sig, contract, risk, state)
    ticket = build_ticket(sig, sizing, contract, risk)
    json_path, md_path = write_ticket(ticket, args.out)
    print(json.dumps(ticket, ensure_ascii=False, indent=2))
    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")
    return 0


def _add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--bars", required=True, help="OHLCV CSV path")
    parser.add_argument("--symbol", required=True, help="Symbol key in contracts JSON")
    parser.add_argument("--config", default="config.example.json", help="Config JSON path")
    parser.add_argument("--contracts", default="contracts.example.json", help="Contracts JSON path")
    parser.add_argument("--out", default="runs/latest", help="Output directory")
    parser.add_argument("--state", default=None, help="Optional account state JSON for kill switches")


def _size_with_kill_switches(signal, contract, risk, state):
    if state is None:
        return size_order(signal, contract, risk)
    risk_budget = state.current_equity * risk.risk_per_trade_fraction
    if daily_loss_exceeded(state.realized_pnl_today, risk, state.current_equity):
        return OrderSizing(False, 0, "daily_loss_kill_switch", risk_budget, 0.0, 0.0, 0.0)
    if drawdown_exceeded(state.peak_equity, state.current_equity, risk):
        return OrderSizing(False, 0, "drawdown_kill_switch", risk_budget, 0.0, 0.0, 0.0)
    return size_order(
        signal,
        contract,
        risk,
        equity=state.current_equity,
        open_margin=state.open_margin,
    )


def screen_universe(universe_path, contracts_path, risk, strategy, state) -> dict[str, Any]:
    root = Path(universe_path).resolve().parent
    payload = load_json(universe_path)
    rows = []
    for candidate in payload.get("candidates", []):
        symbol = candidate["symbol"]
        bars_path = Path(candidate["bars"])
        if not bars_path.is_absolute():
            bars_path = root / bars_path
        try:
            bars = load_bars_csv(bars_path)
            contract = load_contract(contracts_path, symbol)
            sig = latest_signal(bars, symbol, strategy)
            sizing = _size_with_kill_switches(sig, contract, risk, state)
            rows.append(
                {
                    "symbol": symbol,
                    "profile": candidate.get("profile", ""),
                    "status": "READY" if sizing.accepted else "REJECTED",
                    "reject_reason": None if sizing.accepted else sizing.reason,
                    "side": sig.side,
                    "qty": sizing.qty,
                    "entry": sig.entry,
                    "stop": sig.stop,
                    "take_profit": sig.take_profit,
                    "risk_budget": sizing.risk_budget,
                    "risk_per_contract": sizing.risk_per_contract,
                    "margin_required": sizing.margin_required,
                    "reason": sig.reason,
                    "notes": candidate.get("notes", ""),
                }
            )
        except Exception as exc:
            rows.append(
                {
                    "symbol": symbol,
                    "profile": candidate.get("profile", ""),
                    "status": "ERROR",
                    "reject_reason": str(exc),
                    "notes": candidate.get("notes", ""),
                }
            )
    rows.sort(key=lambda r: (0 if r["status"] == "READY" else 1, r["symbol"]))
    ready = [r for r in rows if r["status"] == "READY"]
    return {
        "summary": {
            "candidate_count": len(rows),
            "ready_count": len(ready),
            "decision": "TRADE_REVIEW_ALLOWED" if ready else "NO_TRADE",
            "message": (
                "Only READY candidates may proceed to manual ticket review."
                if ready
                else "No candidate fits current risk and margin settings."
            ),
        },
        "candidates": rows,
    }


def _screen_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# Universe Screen Results",
        "",
        f"Decision: {result['summary']['decision']}",
        f"Candidates: {result['summary']['candidate_count']}",
        f"READY: {result['summary']['ready_count']}",
        "",
        "| Symbol | Status | Side | Qty | Risk/Unit | Risk Budget | Reason |",
        "|---|---|---:|---:|---:|---:|---|",
    ]
    for row in result["candidates"]:
        lines.append(
            "| {symbol} | {status} | {side} | {qty} | {risk_per_contract} | {risk_budget} | {reason} |".format(
                symbol=row.get("symbol", ""),
                status=row.get("status", ""),
                side=row.get("side", ""),
                qty=row.get("qty", ""),
                risk_per_contract=row.get("risk_per_contract", ""),
                risk_budget=row.get("risk_budget", ""),
                reason=row.get("reject_reason") or row.get("reason", ""),
            )
        )
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
