
#-*- coding: utf-8 -*-

# for reading transactions
import pandas as pd

class Depot:
    """Depot handles all buying and selling of stocks."""
    def __init__(self, stock, broker = None, orderbook = None):
        self.orderbook = orderbook
        self.broker = broker
        self.__stock = stock
        self.TAX = 0 # cummulative tax debt

    @property
    def stock(self):
        return self.__stock

    @property
    def orderbook(self):
        return self.__orderbook

    @orderbook.setter
    def orderbook(self, orderbook):
        self.__orderbook = orderbook

    @property
    def broker(self):
        return self.__broker

    @broker.setter
    def broker(self, broker):
        self.__broker = broker

    @property
    def TAX(self):
        return self.__TAX

    @TAX.setter
    def TAX(self, TAX):
        self.__TAX = max(TAX, 0)


    def totalStockinDepot(self):
        #buy_df = pd.DataFrame()
        #sell_df = pd.DataFrame()
        buy_df = self.orderbook.getTransactionByStockAndOrder(self.__stock, 'buy')
        sell_df = self.orderbook.getTransactionByStockAndOrder(self.__stock, 'sell')
        return buy_df['shares'].sum() - sell_df['shares'].sum()

    def buy(self, date, shares, price):
        """
        Steps to buy stocks
        1. Calculate fee; tax is zero
        2. Calculate order volume
        3. Check if sufficient balance available
        3a. insufficient balance: zero transaction
        4. Add order to oderbook
        5. decrease balance on broker ( order volume + fee )
        """
        # step 1
        fee = self.broker.calcFee(shares, price)
        tax = 0
        # step 2
        order_volume = shares * price
        # step 3
        if self.broker.balance < ( order_volume + fee ) :
            # zero transaction
            shares = 0
            fee = 0
            order_volume = shares * price
        # step 4
        self.orderbook.addTransaction(date, 'buy', self.__stock, shares, price, fee)
        self.broker.balance -= order_volume + fee


    def sell(self, date, shares, price):
        """
        Steps to sell stocks
        1. Check amount of stocks available
            a. if insufficient, sell all
        2. Calculate fee;
        3. Calculate order volume
        4. Add order to oderbook
        5. Adjust balance on broker ( order volume - fee )
        6. Calculate tax; ( will reduce balance )
        """
        # step 1
        # sell given shares or all
        total_shares = self.totalStockinDepot()
        shares = min(shares, total_shares)
        # step 2
        fee = self.broker.calcFee(shares, price)
        # step 2
        order_volume = shares * price
        # step 4
        self.orderbook.addTransaction(date, 'sell', self.__stock, shares, price, fee)
        # step 5
        self.broker.balance += (order_volume - fee)
        # step 6
        #self.broker.calcTax(self.orderbook)
