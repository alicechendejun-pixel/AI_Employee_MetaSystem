import unittest

from mlt.models import Bar, StrategyConfig
from mlt.strategy import latest_signal


class StrategyTests(unittest.TestCase):
    def test_latest_signal_long_breakout(self):
        bars = [
            Bar(str(i), 100 + i, 101 + i, 99 + i, 100 + i)
            for i in range(12)
        ]
        bars[-1] = Bar("breakout", 120.0, 123.0, 119.0, 122.0)
        cfg = StrategyConfig(entry_lookback=5, atr_period=3, trend_sma_period=5, atr_stop_multiple=2.0)

        signal = latest_signal(bars, "X", cfg)

        self.assertEqual(signal.side, "LONG")
        self.assertIsNotNone(signal.stop)
        self.assertIsNotNone(signal.take_profit)

    def test_latest_signal_flat_without_history(self):
        bars = [Bar("1", 1, 2, 0.5, 1.5)]
        cfg = StrategyConfig(entry_lookback=5, atr_period=3, trend_sma_period=5)

        signal = latest_signal(bars, "X", cfg)

        self.assertEqual(signal.side, "FLAT")


if __name__ == "__main__":
    unittest.main()

