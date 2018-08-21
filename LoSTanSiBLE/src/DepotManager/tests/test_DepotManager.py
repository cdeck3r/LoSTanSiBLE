#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `DepotManager` package."""

import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

import pytest

# required classes
from DepotManager import DepotManager

import datetime as dt


def test_DepotManager():
    dpMng = DepotManager()
    # Create an APPL depot
    depotAPPL = dpMng.builtDepot('APPL')
    # charge the broker's balanace
    depotAPPL.broker.balance = 1000
    assert depotAPPL.broker.balance == 1000

    # buy some stocks
    depotAPPL.buy(dt.datetime.now().date(), 10, 10 )
    assert depotAPPL.totalStockinDepot() == 10
    # balance is less than initial balance - costs - fees
    assert depotAPPL.broker.balance < 1000-10*10

    # sell all stocks
    depotAPPL.sell(dt.datetime.now().date(), 10000, 10)
    assert depotAPPL.totalStockinDepot() == 0
    # balance is less than initial balance, because of fees
    assert depotAPPL.broker.balance < 1000

    # no profit, no tax
    assert depotAPPL.TAX == 0
