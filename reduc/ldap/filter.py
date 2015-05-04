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

class Filter:
    def __str__(self):
        raise NotImplementedError


class Eq(Filter):
    def __init__(self, key, val):
        self.key = key
        self.val = val

    def __str__(self):
        return '({0.key}={0.val})'.format(self)


class Not(Filter):
    def __init__(self, filter):
        self.filter = filter

    def __str__(self):
        return '(!{0})'.format(str(filter))


class FilterList(Filter):
    def __init__(self, *filters):
        assert filters
        self.filters = filters

    def _symbol(self):
        raise NotImplementedError

    def _filterList(self):
        return ''.join([str(x) for x in self.filters])

    def __str__(self):
        if len(self.filters) == 1:
            return str(self.filters[0])
        else:
            return '({0}{1})'.format(self._symbol(), self._filterList())


class And(FilterList):
    def _symbol(self):
        return '&'


class Or(FilterList):
    def _symbol(self):
        return '|'
