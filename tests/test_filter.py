#! /usr/bin/env python
# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2010. Jose Dinuncio
# All Rights Reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License.
#
##############################################################################
import unittest
from reduc.ldap.filter import *

class TestFilter(unittest.TestCase):
    def setUp(self):
        self.eq1 = Eq('key1', 'val1')
        self.eq2 = Eq('key2', 'val2')
        self.eq3 = Eq('key3', 'val3')


class TestEq(TestFilter):
    def test_eq(self):
        '''Tests Eq filter'''
        rep = str(self.eq1)
        assert '(key1=val1)' == rep, rep


class TestFilterList(TestFilter):
    def test_emptyList(self):
        '''Tests FilterList with empty list'''
        self.assertRaises(AssertionError, FilterList)

    def test_filterList(self):
        '''Tests FilterList._filterList'''
        filter = FilterList(self.eq1, self.eq2)
        rep = filter._filterList()
        assert '(key1=val1)(key2=val2)' == rep, rep

    def testFilterWithOneElement(self):
        '''Tests FilterList filter with one element'''
        filter = FilterList(self.eq1)
        rep = str(filter)
        assert '(key1=val1)' == rep, rep


class TestAnd(TestFilter):
    def testListWithTwoElements(self):
        '''Tests And filter with two elements'''
        filter = And(self.eq1, self.eq2)
        rep = str(filter)
        assert '(&(key1=val1)(key2=val2))' == rep, rep


class TestOr(TestFilter):
    def testListWithTwoElements(self):
        '''Tests Or filter with two elements'''
        filter = Or(self.eq1, self.eq2)
        rep = str(filter)
        assert '(|(key1=val1)(key2=val2))' == rep, rep

