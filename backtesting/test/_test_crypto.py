from unittest import TestCase
from unittest.mock import patch
from backtesting import Backtest, Strategy
from backtesting.lib import (
    OHLCV_AGG,
    SignalStrategy,
    TrailingStrategy,
    barssince,
    compute_stats,
    cross,
    crossover,
    plot_heatmaps,
    quantile,
    random_ohlc_data,
    resample_apply,
)
from backtesting.test import SMA, BTCUSDT

class SmaCross(Strategy):
    # NOTE: These values are also used on the website!
    fast = 10
    slow = 30

    def init(self):
        self.sma1 = self.I(SMA, self.data.Close, self.fast)
        self.sma2 = self.I(SMA, self.data.Close, self.slow)

    def next(self):
        if crossover(self.sma1, self.sma2):
            self.position.close()
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.position.close()
            self.sell()

class TestCryptoBackTest(TestCase):

    def test_run(self):
        bt = Backtest(BTCUSDT, SmaCross, cash=10000)
        bt.run()
        self.assertNotEqual(len(bt._results['_trades']), 0)
