from __future__ import annotations

import argparse
import json
import threading
import time
from pathlib import Path
from typing import Any

from ibapi.client import EClient
from ibapi.wrapper import EWrapper


LIVE_PORTS = {7496, 4001}
PAPER_PORTS = {7497, 4002}


class ReadOnlyProbe(EWrapper, EClient):
    def __init__(self) -> None:
        EClient.__init__(self, self)
        self.ready = threading.Event()
        self.done = threading.Event()
        self.payload: dict[str, Any] = {
            "connected": False,
            "next_valid_order_id": None,
            "managed_accounts": [],
            "account_summary": {},
            "positions": [],
            "open_orders_seen": 0,
            "errors": [],
        }

    def nextValidId(self, orderId: int) -> None:
        self.payload["connected"] = True
        self.payload["next_valid_order_id"] = orderId
        self.ready.set()

    def managedAccounts(self, accountsList: str) -> None:
        self.payload["managed_accounts"] = [x for x in accountsList.split(",") if x]

    def accountSummary(self, reqId: int, account: str, tag: str, value: str, currency: str) -> None:
        self.payload["account_summary"].setdefault(account, {})[tag] = {
            "value": value,
            "currency": currency,
        }

    def accountSummaryEnd(self, reqId: int) -> None:
        self.done.set()

    def position(self, account: str, contract, position: float, avgCost: float) -> None:
        self.payload["positions"].append(
            {
                "account": account,
                "symbol": getattr(contract, "symbol", ""),
                "secType": getattr(contract, "secType", ""),
                "currency": getattr(contract, "currency", ""),
                "exchange": getattr(contract, "exchange", ""),
                "position": position,
                "avgCost": avgCost,
            }
        )

    def openOrder(self, orderId, contract, order, orderState) -> None:
        self.payload["open_orders_seen"] += 1

    def error(self, reqId, errorCode, errorString, advancedOrderRejectJson="") -> None:
        self.payload["errors"].append(
            {
                "reqId": reqId,
                "code": errorCode,
                "message": errorString,
                "advanced": advancedOrderRejectJson,
            }
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only IBKR Paper probe")
    parser.add_argument("--config", default="config.ibkr_paper.template.json")
    parser.add_argument("--out", default="runs/ibkr_readonly_probe")
    parser.add_argument("--timeout", type=float, default=8.0)
    args = parser.parse_args()

    config = json.loads(Path(args.config).read_text(encoding="utf-8"))
    host = config.get("host", "127.0.0.1")
    port = int(config.get("tws_paper_port", 7497))
    client_id = int(config.get("client_id", 77))

    if port in LIVE_PORTS and not config.get("allow_live_ports", False):
        raise SystemExit(f"Refusing to connect to live IBKR port {port}")
    if port not in PAPER_PORTS:
        raise SystemExit(f"Refusing non-paper port {port}; expected one of {sorted(PAPER_PORTS)}")

    app = ReadOnlyProbe()
    app.connect(host, port, client_id)
    thread = threading.Thread(target=app.run, daemon=True)
    thread.start()

    if not app.ready.wait(args.timeout):
        app.disconnect()
        _write(args.out, app.payload)
        print(json.dumps(app.payload, ensure_ascii=False, indent=2))
        return 2

    app.reqManagedAccts()
    app.reqPositions()
    app.reqOpenOrders()
    app.reqAccountSummary(9001, "All", "NetLiquidation,TotalCashValue,AvailableFunds,BuyingPower")
    app.done.wait(args.timeout)
    time.sleep(1.0)
    app.cancelAccountSummary(9001)
    app.cancelPositions()
    app.disconnect()

    _write(args.out, app.payload)
    print(json.dumps(app.payload, ensure_ascii=False, indent=2))
    return 0 if app.payload["connected"] else 2


def _write(outdir: str, payload: dict[str, Any]) -> None:
    target = Path(outdir)
    target.mkdir(parents=True, exist_ok=True)
    (target / "ibkr_readonly_probe.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    raise SystemExit(main())

