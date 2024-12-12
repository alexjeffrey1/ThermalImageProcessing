#!bin/env python3.8
# -*- coding: utf-8 -*-
"""
otherfunctions.py holds some other functions, used in more scripts
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

import numpy as np


def calc_equation(z, x):
    """
    y = calc_equation(z, x)
    Input z, list of function variables
    """
    k = range(0, len(z))
    m = k[::-1]
    y = 0
    for i in k:
        y += np.multiply(z[i], x ** m[i])
    return y


def maxloc(t):
    maximum = 0
    rownr = -1
    rownrmax = 0
    for row in t:
        rownr += 1
        maxi = max(row)
        if maxi > maximum:
            maximum = maxi
            rownrmax = rownr
    maxt = maximum
    maximum = 0
    collnr = -1
    collnrmax = 0
    for i in t[rownrmax]:
        collnr += 1
        if i > maximum:
            maximum = i
            collnrmax = collnr
    if maximum > maxt:
        maxt = maximum
    return collnrmax, rownrmax, maxt


def minloc(t):
    minimum = 1000000
    rownr = -1
    rownrmin = 0
    for row in t:
        rownr += 1
        mini = min(row)
        if mini < minimum:
            minimum = mini
            rownrmin = rownr
    mint = minimum
    minimum = 1000000
    collnr = -1
    collnrmin = 0
    for i in t[rownrmin]:
        collnr += 1
        if i < minimum:
            minimum = i
            collnrmin = collnr
    if minimum < mint:
        mint = minimum
    return collnrmin, rownrmin, mint
