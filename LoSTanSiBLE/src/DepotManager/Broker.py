
#-*- coding: utf-8 -*-

import abc


class Broker:
    """Broker takes care of taxes and fees."""

    __metaclass__ = abc.ABCMeta

    __TAX_rate = 0.25

    def __init__(self, balance = 0):
        self.balance = balance

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, balance):
        self.__balance = balance

    def calcTax(self, orderbook, stock):
        """ Computes the tax across the orderbook """

        """
        Steps to calc taxes
        see: https://github.com/cdeck3r/LoSTanSiBLE/wiki/taxcalculation
        """
        tot_buy_stocks = orderbook.getTransactionByStockAndOrder(stock, 'buy')
        tot_sell_stocks = orderbook.getTransactionByStockAndOrder(stock, 'sell')
        tot_buy = tot_buy_stocks[['shares', 'price']].product(axis=1).sum()
        tot_sell = tot_sell_stocks[['shares', 'price']].product(axis=1).sum()

        # last order is a sell transaction, this is what we have expected
        # we take the price to calc the depot
        tot_shares_depot = tot_buy_stocks['shares'].sum() - tot_sell_stocks['shares'].sum()
        #tot_depot = last_trans['price'].values[0] * tot_shares_depot # stocks in depot
        tot_depot = tot_buy_stocks['price'].mean() * tot_shares_depot # stocks in depot

        gross_profit = tot_sell - (tot_buy - tot_depot)

        return self.__TAX_rate * gross_profit


    @abc.abstractmethod
    def calcFee(self, shares, price):
        """ calculates fees of a transaction """
