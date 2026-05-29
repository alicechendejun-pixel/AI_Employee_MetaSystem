import unittest

from mlt.models import ContractSpec, RiskConfig, Signal
from mlt.risk import daily_loss_exceeded, drawdown_exceeded, size_order


class RiskTests(unittest.TestCase):
    def test_size_order_uses_risk_and_margin_caps(self):
        signal = Signal("X", "2026-01-01", "LONG", 100.0, 98.0, 104.0, "test")
        contract = ContractSpec("X", multiplier=10.0, tick_size=1.0, margin_rate=0.1)
        risk = RiskConfig(
            capital=10000.0,
            risk_per_trade_fraction=0.01,
            max_margin_fraction=0.5,
            commission_per_contract=0.0,
            slippage_ticks=0.0,
        )

        sizing = size_order(signal, contract, risk)

        self.assertTrue(sizing.accepted)
        self.assertEqual(sizing.qty, 5)
        self.assertEqual(sizing.risk_per_contract, 20.0)
        self.assertEqual(sizing.margin_required, 500.0)

    def test_reject_when_stop_risk_exceeds_budget(self):
        signal = Signal("X", "2026-01-01", "LONG", 100.0, 50.0, 200.0, "test")
        contract = ContractSpec("X", multiplier=10.0, tick_size=1.0, margin_rate=0.1)
        risk = RiskConfig(capital=10000.0, risk_per_trade_fraction=0.005)

        sizing = size_order(signal, contract, risk)

        self.assertFalse(sizing.accepted)
        self.assertEqual(sizing.reason, "risk_budget_too_small")

    def test_kill_switches(self):
        risk = RiskConfig(capital=10000.0, max_daily_loss_fraction=0.015, max_total_drawdown_fraction=0.08)
        self.assertTrue(daily_loss_exceeded(-151.0, risk))
        self.assertFalse(daily_loss_exceeded(-149.0, risk))
        self.assertTrue(drawdown_exceeded(10000.0, 9100.0, risk))
        self.assertFalse(drawdown_exceeded(10000.0, 9300.0, risk))

    def test_size_order_respects_lot_step(self):
        signal = Signal("ETF", "2026-01-01", "LONG", 1.12, 1.04, 1.28, "test")
        contract = ContractSpec("ETF", multiplier=1.0, tick_size=0.001, margin_rate=1.0, min_qty=100, lot_step=100)
        risk = RiskConfig(
            capital=10000.0,
            risk_per_trade_fraction=0.005,
            max_margin_fraction=0.35,
            commission_per_contract=0.0,
            slippage_ticks=0.0,
        )

        sizing = size_order(signal, contract, risk)

        self.assertTrue(sizing.accepted)
        self.assertEqual(sizing.qty % 100, 0)

    def test_flat_reject_reports_real_risk_budget(self):
        signal = Signal("X", "2026-01-01", "FLAT", 100.0, None, None, "test")
        contract = ContractSpec("X", multiplier=10.0, tick_size=1.0, margin_rate=0.1)
        risk = RiskConfig(capital=10000.0, risk_per_trade_fraction=0.005)

        sizing = size_order(signal, contract, risk)

        self.assertFalse(sizing.accepted)
        self.assertEqual(sizing.risk_budget, 50.0)


if __name__ == "__main__":
    unittest.main()
