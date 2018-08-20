#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `Depot` package."""

import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

import pytest

from DepotBuilder import DepotBuilder

import pandas as pd

import datetime as dt


@pytest.fixture
def depot():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')
    return DepotBuilder('APPL').getDepot()

def test_balance(depot):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
    balance = depot.broker.balance
    assert balance == 0

def test_orderbook(depot):
    transactions = depot.orderbook.totalTransactions()
    assert transactions == 1

def test_balance_change(depot):
    depot.broker.balance = 1000
    balance = depot.broker.balance
    assert balance == 1000

def test_transaction(depot):
    depot.orderbook.addTransaction()
    transactions = depot.orderbook.totalTransactions()
    assert transactions == 2

def test_transaction_params(depot):
    depot.orderbook.addTransaction()
    depot.orderbook.addTransaction(shares=100, price=10)
    transactions = depot.orderbook.totalTransactions()
    assert transactions == 3

def test_transaction_last(depot):
    depot.orderbook.addTransaction()
    depot.orderbook.addTransaction()

    transactions = depot.orderbook.totalTransactions()
    assert transactions == 3

    df = depot.orderbook.getLastTransaction()
    assert df.index.values[0] == 2

def test_transaction_1000(depot):
    depot.orderbook.addTransaction()
    depot.orderbook.addTransaction()
    # will return the last transaction
    df = depot.orderbook.getTransactionByIndex(1000)
    assert df.index.values[0] == 2

def test_transaction_1(depot):
    depot.orderbook.addTransaction()
    depot.orderbook.addTransaction()
    pd.df = depot.orderbook.getTransactionByIndex(1)
    assert pd.df.index.values[0] == 1

def test_buy_order(depot):
    depot.broker.balance = 1000
    depot.buy(dt.datetime.now().date(), 10, 10 )
    # assert one transaction more than initial
    transactions = depot.orderbook.totalTransactions()
    assert transactions == 2
    # assert balance
    balance = depot.broker.balance
    assert balance < 1000-100
    # assert number of buy transactions
    df = depot.orderbook.getTransactionByStockAndOrder(depot.stock, 'buy')
    buy_transactions = df.shape[0]
    assert buy_transactions == 1

def test_sell_order(depot):
    depot.broker.balance = 1000
    # buy 10; volume 100
    depot.buy(dt.datetime.now().date(), 10, 10 )
    # assert one transaction more than initial
    transactions = depot.orderbook.totalTransactions()
    assert transactions == 2
    # assert balance
    balance = depot.broker.balance
    assert balance < 1000-100
    # assert total_shares
    total_shares = depot.totalStockinDepot()
    assert total_shares == 10

    # sell 5; volume 50
    depot.sell(dt.datetime.now().date(), 5, 10)
    transactions = depot.orderbook.totalTransactions()
    assert transactions == 3
    # assert balance
    balance = depot.broker.balance
    assert balance > 1000-100
    assert balance < 1000
    # assert total_shares
    total_shares = depot.totalStockinDepot()
    assert total_shares == 5
    # assert number of buy transactions
    df = depot.orderbook.getTransactionByStockAndOrder(depot.stock, 'buy')
    buy_transactions = df.shape[0]
    assert buy_transactions == 1
    # assert number of sell transactions
    df = depot.orderbook.getTransactionByStockAndOrder(depot.stock, 'sell')
    buy_transactions = df.shape[0]
    assert buy_transactions == 1


    # sell more than avail (equals all); volume 50
    depot.sell(dt.datetime.now().date(), 50000, 10)
    transactions = depot.orderbook.totalTransactions()
    assert transactions == 4
    # assert balance
    balance = depot.broker.balance
    assert balance < 1000
    assert balance > 1000-100
    # assert total_shares
    total_shares = depot.totalStockinDepot()
    assert total_shares == 0

def test_tax(depot):
    depot.broker.balance = 1000
    # buy 10; price 10; volume 100
    depot.buy(dt.datetime.now().date(), 10, 10 )
    # assert one transaction more than initial
    transactions = depot.orderbook.totalTransactions()
    assert transactions == 2
    # assert balance
    balance = depot.broker.balance
    assert balance < 1000-100
    # assert total_shares
    total_shares = depot.totalStockinDepot()
    assert total_shares == 10
    # test TAX; first buy -> no tax
    assert depot.TAX == 0

    # sell all: sell 10; price 10.5; volume 105 (5% gross_profit)
    depot.sell(dt.datetime.now().date(), 10, 10.5)
    transactions = depot.orderbook.totalTransactions()
    assert transactions == 3
    # assert balance
    balance = depot.broker.balance
    assert balance > 1000-100
    assert balance < 1000
    # assert total_shares
    total_shares = depot.totalStockinDepot()
    assert total_shares == 0
    # assert TAX > 0
    depot.TAX == 1.25

    depot.broker.balance = 1000
    # buy 10; price 10; volume 100
    depot.buy(dt.datetime.now().date(), 10, 10 )
    # sell all: sell 10; price 9.5; volume 95 (5% loss)
    depot.sell(dt.datetime.now().date(), 10, 9.5)
    # assert total_shares
    total_shares = depot.totalStockinDepot()
    assert total_shares == 0
    # assert TAX == 0, because we had the same win and loss
    assert depot.TAX == 0

def test_multiorder_tax_loss_and_profits(depot):
    # initialize balance
    depot.broker.balance = 1000

    # buy 10; price 10; volume 100
    depot.buy(dt.datetime.now().date(), 10, 10 )
    # buy 10; price 10; volume 100
    depot.buy(dt.datetime.now().date(), 10, 10 )
    # sell 10; price 10; volume 100
    depot.sell(dt.datetime.now().date(), 10, 10)
    # assert total_shares; we have stocks in the depot
    total_shares = depot.totalStockinDepot()
    assert total_shares == 10
    # we expect not to pay tax
    assert depot.TAX == 0

    # buy again 10; price 10; volume 100
    depot.buy(dt.datetime.now().date(), 10, 10 )
    # sell 10; price 9.5; volume 95 (5% loss)
    depot.sell(dt.datetime.now().date(), 10, 9.5)
    # assert total_shares; we have stocks in the depot
    total_shares = depot.totalStockinDepot()
    assert total_shares == 10
    # we expect not to pay tax, because we made an overall loss
    assert depot.TAX == 0

    # buy again 10; price 10; volume 100
    depot.buy(dt.datetime.now().date(), 10, 10 )
    # sell 10; price 10.5; volume 105 (5% profit)
    depot.sell(dt.datetime.now().date(), 10, 10.5)
    # assert total_shares; we have stocks in the depot
    total_shares = depot.totalStockinDepot()
    assert total_shares == 10
    # we do not expect pay tax; we made overall a 5% loss and 5% win
    assert depot.TAX == 0

def test_multiorder_tax_profits(depot):
    # initialize balance
    depot.broker.balance = 1000

    # buy 10; price 10; volume 100
    depot.buy(dt.datetime.now().date(), 10, 10 )
    # buy 10; price 10; volume 100
    depot.buy(dt.datetime.now().date(), 10, 10 )
    # sell 10; price 10; volume 100
    depot.sell(dt.datetime.now().date(), 10, 10.5)
    # assert total_shares; we have stocks in the depot
    total_shares = depot.totalStockinDepot()
    assert total_shares == 10
    # pay tax on 5% profit
    assert depot.TAX == 1.25

    depot.buy(dt.datetime.now().date(), 10, 10 )
    # sell 10; price 10; volume 100
    depot.sell(dt.datetime.now().date(), 10, 10.5)
    # assert total_shares; we have stocks in the depot
    total_shares = depot.totalStockinDepot()
    assert total_shares == 10
    # pay tax on another 5% profit
    assert depot.TAX == 2.5 # overall tax paid

def test_multiorder_tax_neutral(depot):
    # we test the tax calc when buying and selling
    # different shares and prices

    # initialize balance
    depot.broker.balance = 1000

    # buy 30; price 10; volume 300
    depot.buy(dt.datetime.now().date(), 50, 10 )
    # assert balance
    assert depot.broker.balance < 1000-500
    # sell 10; price 9.5; volume 95
    depot.sell(dt.datetime.now().date(), 10, 9.5)
    # assert balance
    assert depot.broker.balance < 1000-500+95
    # sell 10; price 9.5; volume 95
    depot.sell(dt.datetime.now().date(), 10, 9.5)
    # assert balance
    assert depot.broker.balance < 1000-500+95+95
    # buy 10; price 11; volume 110
    depot.buy(dt.datetime.now().date(), 10, 11)
    # assert balance
    assert depot.broker.balance < 1000-500+95+95-110
    # assert total_shares; we have stocks in the depot
    total_shares = depot.totalStockinDepot()
    assert total_shares == 40
    # pay tax on another 5% profit
    assert depot.TAX == 0 # overall tax paid
