import json
import sys
import time
import threading
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order

class IBKRPaperTicketExecutor(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.next_order_id = None

    def nextValidId(self, orderId: int):
        self.next_order_id = orderId
        print(f"✅ Next valid order ID: {orderId}")

    def error(self, reqId, errorCode, errorString):
        if errorCode not in [2104, 2106, 2158]:
            print(f"❌ IBKR Error {errorCode}: {errorString}")

    def orderStatus(self, orderId, status, filled, remaining, avgFillPrice, permId,
                    parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
        print(f"📊 Order {orderId} Status: {status}")


def load_ticket(ticket_path):
    with open(ticket_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def main():
    if len(sys.argv) < 2:
        print("Usage: python broker_adapters\\ibkr_paper_ticket_executor.py <ticket_json_path>")
        sys.exit(1)

    ticket = load_ticket(sys.argv[1])

    if ticket.get("status") != "READY":
        print("❌ Ticket is not READY.")
        return

    print(f"🚀 Executing TSLA Paper: {ticket['side']} {ticket['qty']} TSLA")

    app = IBKRPaperTicketExecutor()
    app.connect("127.0.0.1", 7497, clientId=201)

    api_thread = threading.Thread(target=app.run, daemon=True)
    api_thread.start()

    time.sleep(3)

    if app.next_order_id is None:
        print("❌ Cannot connect to TWS.")
        app.disconnect()
        return

    # TSLA Contract (Stock)
    contract = Contract()
    contract.symbol = "TSLA"
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"

    parent = Order()
    parent.orderId = app.next_order_id
    parent.action = "BUY" if ticket["side"] == "LONG" else "SELL"
    parent.orderType = "MKT"
    parent.totalQuantity = ticket["qty"]
    parent.eTradeOnly = False
    parent.firmQuoteOnly = False
    parent.transmit = False

    stop = Order()
    stop.orderId = app.next_order_id + 1
    stop.action = "SELL" if parent.action == "BUY" else "BUY"
    stop.orderType = "STP"
    stop.auxPrice = ticket["stop"]
    stop.totalQuantity = ticket["qty"]
    stop.eTradeOnly = False
    stop.firmQuoteOnly = False
    stop.parentId = app.next_order_id
    stop.transmit = True

    print("📤 Sending Market Entry + Stop to TWS Paper...")

    app.placeOrder(parent.orderId, contract, parent)
    time.sleep(1.5)
    app.placeOrder(stop.orderId, contract, stop)

    print("✅ Orders sent! 请立即切换到 TWS Paper 窗口查看 TSLA 订单。")

    time.sleep(8)
    app.disconnect()


if __name__ == "__main__":
    main()