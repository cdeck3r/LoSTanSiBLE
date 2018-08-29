#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `DepotManager` package."""

import sys, os
this_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, this_dir + '/../')


import pytest
import pandas as pd

# required classes
from DataShelf import DataShelf

shelf_name = 'testshelf'

@pytest.fixture(scope='function')
def setup_shelf():
    shelf_filepath = os.path.join(this_dir, shelf_name)

    # delete any previous shelf file
    if os.path.exists(shelf_filepath + '.db'):
        os.remove(shelf_filepath + '.db')

    DataShelf.shelf_filepath = shelf_filepath


def test_DataShelf(setup_shelf):
    # we test the basic func. - storing and loading a record
    DataShelf.put_in_shelf('key_0', 'val_0')
    df = DataShelf.get_from_shelf()
    assert 'key_0' == df.at[0,'key']
    assert 'val_0' == df.at[0,'val']
    assert 'record' == df.at[0,'type']

def test_DataShelf_namedrecord(setup_shelf):
    DataShelf.clear_shelf()

    # storing and loading a record with a name
    DataShelf.put_in_shelf('key_0', 'val_0', 'parameter')
    df = DataShelf.get_from_shelf()
    assert 'key_0' == df.at[0,'key']
    assert 'val_0' == df.at[0,'val']
    assert 'parameter' == df.at[0,'type']

def test_DataShelf_multirecord(setup_shelf):
    DataShelf.clear_shelf()

    # storing and loading a record with a name
    DataShelf.put_in_shelf('key_0', 'val_0')
    DataShelf.put_in_shelf('key_1', 'val_1')
    DataShelf.put_in_shelf('key_2', 'val_2', 'parameter')

    df = DataShelf.get_from_shelf()

    for i in df.index:
        assert 'key_'+str(i) == df.at[i,'key']
        assert 'val_'+str(i) == df.at[i,'val']

        if i == 2:
            assert 'parameter' == df.at[i,'type']
        else:
            assert 'record' == df.at[i,'type']

    # we put another record in the shelf
    # and get it from it afterwards
    DataShelf.put_in_shelf('key_3', 'val_3')
    df = DataShelf.get_from_shelf()
    i = 3
    assert 'key_'+str(i) == df.at[i,'key']
    assert 'val_'+str(i) == df.at[i,'val']

def test_DataShelf_df(setup_shelf):
    DataShelf.clear_shelf()

    # we store and receive an entire dataframe
    df = pd.DataFrame([[1, 2], [3, 4]], columns=list('AB'))
    DataShelf.put_in_shelf_df('myDF', df)
    rcvDF = DataShelf.get_from_shelf_df('myDF')

    assert df.equals(rcvDF) == True

def test_DataShelf_clearshelf(setup_shelf):
    DataShelf.clear_shelf()
    # we put a record in the shelf
    DataShelf.put_in_shelf('key_0', 'val_0')
    # we store an entire dataframe
    df = pd.DataFrame([[1, 2], [3, 4]], columns=list('AB'))
    DataShelf.put_in_shelf_df('myDF', df)

    # only clears the shelf, but not the entire file
    DataShelf.clear_shelf()
    defaultDF = DataShelf.get_from_shelf()
    # assert for empty default df
    assert defaultDF.equals(pd.DataFrame(columns=['type', 'key', 'val','filename']))

    # myDF DataFrame remains in the shelf
    rcvDF = DataShelf.get_from_shelf_df('myDF')
    assert df.equals(rcvDF) == True


def test_DataShelf_clearall_but_not_defaultshelf(setup_shelf):
    DataShelf.clear_shelf()

    # we put a record in the shelf
    DataShelf.put_in_shelf('key_0', 'val_0')
    # we store an entire dataframe
    df = pd.DataFrame([[1, 2], [3, 4]], columns=list('AB'))
    DataShelf.put_in_shelf_df('myDF', df)

    # only clears the file, but not the internal df
    DataShelf.clear_shelf_file(clearshelf=False)

    defaultDF = DataShelf.get_from_shelf()

    # assert for shelf content
    assert 'key_0' == defaultDF.at[0,'key']
    assert 'val_0' == defaultDF.at[0,'val']
    assert 'record' == defaultDF.at[0,'type']

def test_DataShelf_clearall(setup_shelf):
    DataShelf.clear_shelf()

    # we put a record in the shelf
    DataShelf.put_in_shelf('key_0', 'val_0')
    # we store an entire dataframe
    df = pd.DataFrame([[1, 2], [3, 4]], columns=list('AB'))
    DataShelf.put_in_shelf_df('myDF', df)

    DataShelf.clear_shelf_file()
    rcvDF = DataShelf.get_from_shelf()
    # assert for empty default df
    assert rcvDF.equals(pd.DataFrame(columns=['type', 'key', 'val','filename']))

def test_DataShelf_indexlist(setup_shelf):
    DataShelf.clear_shelf()

    # we put a record in the shelf
    DataShelf.put_in_shelf('key_0', 'val_0')
    # we store an entire dataframe
    df = pd.DataFrame([[1, 2], [3, 4]], columns=list('AB'))
    DataShelf.put_in_shelf_df('myDF', df)

    # get index list
    lst = DataShelf.indexlist()
    refLst = [shelf_name, 'myDF']
    assert lst.sort() == refLst.sort()
