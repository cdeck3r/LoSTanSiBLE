
#-*- coding: utf-8 -*-

import datetime as dt
#import numpy as np
import pandas as pd


class OrderBook:
    """Records all transactions"""
    def __init__(self):
        #self.d = {'one' : [1., 2., 3., 4.], 'two' : [4., 3., 2., 1.]}
        #self.transactions = pd.DataFrame(self.d)
        todays_date = dt.datetime.now().date()
        columns = ['date', 'order', 'stock', 'shares', 'price', 'fee']
        initial_data = [todays_date, 'none', None, 0, 0, 0]
        self.transactions = pd.DataFrame([initial_data], columns=columns)

    def totalTransactions(self):
        return self.transactions.shape[0]

    def addTransaction(self, date=dt.datetime.now().date(), order='buy', stock=None, shares=0, price=0, fee=0):
        data = [date, order, stock, shares, price, fee]
        cols = self.transactions.columns
        self.transactions = self.transactions.append(pd.DataFrame([data], columns=cols))

    def getTransactionByStockAndOrder(self, stock, order):
        stock_transactions = self.getTransactionByStock(stock)
        return stock_transactions.loc[stock_transactions['order'] == order]

    def getTransactionByStock(self, stock):
        return self.transactions.loc[self.transactions['stock'] == stock]

    def getTransactionByOrder(self, order):
        return self.transactions.loc[self.transactions['order'] == order]

    def getTransactionByIndex(self, index):
        if index < self.totalTransactions() :
            return self.transactions.iloc[[index]].reindex([index])
        else:
            return self.getLastTransaction()

    def getLastTransaction(self):
        lastIndex = self.totalTransactions()-1
        pd.df = self.transactions.iloc[[lastIndex]]
        return pd.df.reindex([lastIndex])
