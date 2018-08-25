
#-*- coding: utf-8 -*-

from Broker import Broker
from comdirect import comdirect
from Depot import Depot
from OrderBook import OrderBook

class DepotManager:
    """ Build and acts on depots.

        The default tax rate for all depots is 26.375 %.
        See: https://de.wikipedia.org/wiki/Kapitalertragsteuer_(Deutschland)#Bemessung_der_Kapitalertragsteuer
    """

    def __init__(self, tax_rate=0.26375, broker=comdirect(), orderbook=OrderBook()):
        """ Initialize all depots.

            All depots utilize the same Broker's tax rate,
            comdirect as default broker and orderbook.
        """
        Broker.setTAXRate(tax_rate)
        self.__broker = broker
        self.__orderbook = orderbook

    def buildDepot(self, stock):
        """ Builds the Depot. """
        depot = Depot(stock=stock, broker=self.__broker, orderbook=self.__orderbook)
        return depot

    def run(self):
        pass

if __name__ == '__main__':
    DepotManager().run()
