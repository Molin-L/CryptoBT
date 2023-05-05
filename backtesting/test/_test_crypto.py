from unittest import TestCase

from backtesting import Backtest, Strategy
from backtesting.lib import (
    crossover,
)
from backtesting.idl import Side
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
            self.position().close()
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.position().close()
            self.sell()

class SmaCrossHedging(Strategy):
    # NOTE: These values are also used on the website!
    fast = 10
    slow = 30

    def init(self):
        self.sma1 = self.I(SMA, self.data.Close, self.fast)
        self.sma2 = self.I(SMA, self.data.Close, self.slow)

    def next(self):
        if crossover(self.sma1, self.sma2):
            self.position(side=Side.Sell).close()
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.position(side=Side.Buy).close()
            self.sell()



class TestCryptoBackTest(TestCase):

    def test_run(self):
        bt = Backtest(BTCUSDT, SmaCross, cash=10000)
        bt.run()
        self.assertNotEqual(len(bt._results['_trades']), 0)

    def test_hedging_position(self):
        bt = Backtest(BTCUSDT, SmaCrossHedging, cash=10000, hedging=True)
        bt.run()
        self.assertNotEqual(len(bt._results['_trades']), 0)