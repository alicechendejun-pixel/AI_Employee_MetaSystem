from __future__ import annotations

import argparse
import json
import threading
import time
from pathlib import Path
from typing import Any

from ibapi.client import EClient
from ibapi.contract import Contract
from ibapi.order import Order
from ibapi.wrapper import EWrapper


LIVE_PORTS = {7496, 4001}
PAPER_PORTS = {7497, 4002}


class PaperOrderProbe(EWrapper, EClient):
    def __init__(self) -> None:
        EClient.__init__(self, self)
        self.ready = threading.Event()
        self.accounts_ready = threading.Event()
        self.order_seen = threading.Event()
        self.payload: dict[str, Any] = {
            "connected": False,
            "next_valid_order_id": None,
            "managed_accounts": [],
            "placed_order": None,
            "order_status": [],
            "open_orders": [],
            "errors": [],
        }

    def nextValidId(self, orderId: int) -> None:
        self.payload["connected"] = True
        self.payload["next_valid_order_id"] = orderId
        self.ready.set()

    def managedAccounts(self, accountsList: str) -> None:
        self.payload["managed_accounts"] = [x for x in accountsList.split(",") if x]
        self.accounts_ready.set()

    def openOrder(self, orderId, contract, order, orderState) -> None:
        self.payload["open_orders"].append(
            {
                "orderId": orderId,
                "symbol": getattr(contract, "symbol", ""),
                "secType": getattr(contract, "secType", ""),
                "action": getattr(order, "action", ""),
                "orderType": getattr(order, "orderType", ""),
                "totalQuantity": getattr(order, "totalQuantity", ""),
                "lmtPrice": getattr(order, "lmtPrice", ""),
                "transmit": getattr(order, "transmit", ""),
                "status": getattr(orderState, "status", ""),
            }
        )
        if orderId == self.payload.get("next_valid_order_id"):
            self.order_seen.set()

    def orderStatus(
        self,
        orderId,
        status,
        filled,
        remaining,
        avgFillPrice,
        permId,
        parentId,
        lastFillPrice,
        clientId,
        whyHeld,
        mktCapPrice,
    ) -> None:
        self.payload["order_status"].append(
            {
                "orderId": orderId,
                "status": status,
                "filled": filled,
                "remaining": remaining,
                "avgFillPrice": avgFillPrice,
                "whyHeld": whyHeld,
            }
        )

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
    parser = argparse.ArgumentParser(description="IBKR Paper order-write probe")
    parser.add_argument("--config", default="config.ibkr_paper.template.json")
    parser.add_argument("--out", default="runs/ibkr_paper_order_probe")
    parser.add_argument("--symbol", default="AAPL")
    parser.add_argument("--qty", type=float, default=1)
    parser.add_argument("--limit-price", type=float, default=1.0)
    parser.add_argument("--timeout", type=float, default=10.0)
    parser.add_argument("--client-id", type=int, default=None)
    parser.add_argument(
        "--transmit",
        action="store_true",
        help="Actually transmit the paper order. Default is staged/untransmitted.",
    )
    parser.add_argument(
        "--staged",
        action="store_true",
        help="Create an untransmitted staged order instead of a what-if order.",
    )
    parser.add_argument(
        "--confirm-paper-order",
        action="store_true",
        help="Required together with --transmit.",
    )
    args = parser.parse_args()

    config = json.loads(Path(args.config).read_text(encoding="utf-8"))
    host = config.get("host", "127.0.0.1")
    port = int(config.get("tws_paper_port", 7497))
    client_id = args.client_id if args.client_id is not None else int(config.get("client_id", 77)) + 1

    if port in LIVE_PORTS and not config.get("allow_live_ports", False):
        raise SystemExit(f"Refusing to connect to live IBKR port {port}")
    if port not in PAPER_PORTS:
        raise SystemExit(f"Refusing non-paper port {port}; expected one of {sorted(PAPER_PORTS)}")
    if args.transmit and not args.confirm_paper_order:
        raise SystemExit("--transmit requires --confirm-paper-order")

    app = PaperOrderProbe()
    app.connect(host, port, client_id)
    thread = threading.Thread(target=app.run, daemon=True)
    thread.start()

    if not app.ready.wait(args.timeout):
        app.disconnect()
        _write(args.out, app.payload)
        print(json.dumps(app.payload, ensure_ascii=False, indent=2))
        return 2

    app.reqManagedAccts()
    app.accounts_ready.wait(args.timeout)
    accounts = app.payload["managed_accounts"]
    if not accounts or not all(str(a).startswith("DU") for a in accounts):
        app.disconnect()
        raise SystemExit(f"Refusing non-paper account list: {accounts}")

    order_id = int(app.payload["next_valid_order_id"])
    contract = _stock_contract(args.symbol)
    order = _limit_order(
        "BUY",
        args.qty,
        args.limit_price,
        accounts[0],
        transmit=args.transmit,
        what_if=(not args.transmit and not args.staged),
    )
    app.payload["placed_order"] = {
        "orderId": order_id,
        "account": accounts[0],
        "symbol": args.symbol,
        "qty": args.qty,
        "limit_price": args.limit_price,
        "transmit": args.transmit,
        "what_if": bool(getattr(order, "whatIf", False)),
    }

    app.placeOrder(order_id, contract, order)
    app.order_seen.wait(args.timeout)
    time.sleep(1.0)
    if args.transmit:
        app.cancelOrder(order_id, "")
        time.sleep(1.0)
    app.disconnect()

    _write(args.out, app.payload)
    print(json.dumps(app.payload, ensure_ascii=False, indent=2))

    readonly_errors = [e for e in app.payload["errors"] if "只读" in e.get("message", "") or "read-only" in e.get("message", "").lower()]
    if readonly_errors:
        return 3
    return 0 if app.payload["placed_order"] else 2


def _stock_contract(symbol: str) -> Contract:
    c = Contract()
    c.symbol = symbol
    c.secType = "STK"
    c.exchange = "SMART"
    c.currency = "USD"
    return c


def _limit_order(action: str, qty: float, limit_price: float, account: str, transmit: bool, what_if: bool) -> Order:
    o = Order()
    o.action = action
    o.orderType = "LMT"
    o.totalQuantity = qty
    o.lmtPrice = limit_price
    o.tif = "DAY"
    o.account = account
    o.transmit = True if what_if else transmit
    o.whatIf = what_if
    # The pip ibapi build defaults these deprecated flags to True, and recent
    # TWS rejects orders carrying them.
    o.eTradeOnly = False
    o.firmQuoteOnly = False
    return o


def _write(outdir: str, payload: dict[str, Any]) -> None:
    target = Path(outdir)
    target.mkdir(parents=True, exist_ok=True)
    (target / "ibkr_paper_order_probe.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    raise SystemExit(main())
