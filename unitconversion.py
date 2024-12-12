#!bin/env python3.8
# -*- coding: utf-8 -*-
"""
unitconversion.py has common unit conversions in it
Copyright (C) 2021  Roelof Ymker

 This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

def k2c(k):
    """Convert Kelvin to Celsius: c = k2c(k)"""
    c = k - 273.15
    return c


def c2k(c):
    """Convert Celsius to Kelvin: k = c2k(c)"""
    k = c + 273.15
    return k


def c2n(c):
    """Convert Celsius to Newton: n = c2n(c)"""
    n = c * (33.0 / 100.0)
    return n


def n2c(n):
    """Convert Newton to Celsius: c = n2c(n)"""
    c = n * (100.0 / 33.0)
    return c


def c2f(c, diff=False):
    """
    Convert Celsius to Fahrenheit
    If a temperature level is wanted use: f = c2f(c)
    If a temperature difference is wanted: df = c2f(dc, diff=True)
    """
    f = c * (9.0 / 5.0)
    if not diff:
        f += 32
    return f


def f2c(f, diff=False):
    """
    Convert Fahrenheit to Celsius
    If a temperature level is wanted use: c = f2c(f)
    If a temperature difference is wanted: dc = f2c(df, diff=True)
    """
    if not diff:
        f -= 32
    c = f * (5.0 / 9.0)
    return c


def gpm2lpm(gpm):
    """Convert Gallons per minute to liters per minute: lpm = gpm2lpm(gpm)"""
    lpm = gpm * 3.785412
    return lpm


def lpm2gpm(lpm):
    """Convert liters per minute to Gallons per minute: gpm = lpm2gpm(lpm)"""
    gpm = lpm / 3.785412
    return gpm


def psi2bar(psi):
    """Convert PSI to bar: bar = psi2bar(psi)"""
    bar = psi / 14.50377
    return bar


def bar2psi(bar):
    """Convert bar to PSI: psi = bar2psi(bar)"""
    psi = bar * 14.50377
    return psi


def ft2psi(ft):
    """Convert FT to PSI: psi = ft2psi(ft)"""
    psi = ft * 0.43352750192825
    return psi


def psi2ft(psi):
    """Convert PSI to FT: ft = psi2ft(psi)"""
    ft = psi / 0.43352750192825
    return ft
