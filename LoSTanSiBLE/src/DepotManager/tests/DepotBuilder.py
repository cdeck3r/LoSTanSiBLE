
#-*- coding: utf-8 -*-

from comdirect import comdirect
from Depot import Depot
from OrderBook import OrderBook

class DepotBuilder:
    """Acts on Depots"""

    def __init__(self, stock):
        """ First of all, it builds the Depot """
        self.broker = comdirect()
        self.orderbook = OrderBook()
        self.depot = Depot(stock=stock, broker=self.broker, orderbook=self.orderbook)
        #self.bank.balance = 1000

    def run(self):
        #depot = self.getDepot()
        #depot.bank.balance = 1000
        #depot.buy(dt.datetime.now().date(), 'APPL', 10, 10 )
        #depot.sell(dt.datetime.now().date(), 'APPL', 10, 10 )
        pass


    def getDepot(self):
        return self.depot

if __name__ == '__main__':
    DepotBuilder().run()
