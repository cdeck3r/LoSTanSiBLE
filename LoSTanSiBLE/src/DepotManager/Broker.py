
#-*- coding: utf-8 -*-

import abc

# for orderbook
import math
import pandas as pd

class Broker:
    """Broker takes care of taxes and fees."""

    __metaclass__ = abc.ABCMeta

    def __init__(self, balance = 0):
        self.balance = balance

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, balance):
        self.__balance = balance

    def calcTax(self, orderbook):
        """ Computes the tax across the orderbook """

        """
        Steps to calc taxes
        1. search all sell orders with non-numeric tax
        2. tax is 25 percent of order volume
        3. insert tax
        4

        """
        df = orderbook.getTransactionByOrder('sell')
        df = df.loc[df['tax'] == math.nan]
        df['tax'] = 0.25 * df['shares'] * df['price']


    @abc.abstractmethod
    def calcFee(self, shares, price):
        """ calculates fees of a transaction """
