import unittest
from pathlib import Path

from mlt.backtest import run_backtest
from mlt.data import load_bars_csv
from mlt.models import ContractSpec, RiskConfig, StrategyConfig


class BacktestTests(unittest.TestCase):
    def test_backtest_returns_metrics(self):
        root = Path(__file__).resolve().parents[1]
        bars = load_bars_csv(root / "data" / "sample_ohlcv.csv")
        contract = ContractSpec("SAMPLE_FUT", multiplier=10.0, tick_size=1.0, margin_rate=0.12)
        risk = RiskConfig(capital=10000.0, commission_per_contract=0.0, slippage_ticks=0.0)
        strategy = StrategyConfig(entry_lookback=10, atr_period=5, trend_sma_period=10)

        result = run_backtest(bars, "SAMPLE_FUT", contract, risk, strategy)

        self.assertIn("ending_equity", result)
        self.assertIn("trade_count", result)
        self.assertIn("max_drawdown_fraction", result)


if __name__ == "__main__":
    unittest.main()

