
#-*- coding: utf-8 -*-

from Broker import Broker

class comdirect(Broker):

    def __init__(self):
        super(comdirect, self).__init__()

    def calcFee(self, shares, price):
        """ calculates fees of a transaction """
        """
        Die Provision für eine Inlandsorder setzt sich aus einem
        Grundentgelt von 4,90 Euro zzgl. 0,25%  des Ordervolumens zusammen.
        Wir berechnen mindestens 9,90 Euro (bis 2.000 Euro Ordervolumen),
        maximal 59,90 Euro. Zusätzlich fällt ein börsenplatzabhängiges
        Entgelt an. Dieses beträgt am Börsenplatz Xetra 0,0015 %,
        mindestens 1,50 Euro, an den übrigen Börsen 0,0025 %,
        mindestens 2,50 Euro.
        Neben den berechneten Entgelten und Provisionen weisen wir
        zusätzlich fremde Kosten (wie z. B. Maklercourtage) in der
        Wertpapierabrechnung aus.
        """
        order_volume = shares * price

        # special case: no fees, if there is no volume
        if order_volume == 0:
            return 0

        if order_volume <= 2000 :
            fee = 9.9
        else:
            fee = 4.9 + ( 0.25/100 * order_volume )

        return min(fee, 59.90)
