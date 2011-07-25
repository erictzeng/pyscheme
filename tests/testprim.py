"""
Copyright (C) 2011 AUTHORS

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import unittest

from data import IntLiteral as intl
import prim

class PrimitiveSuccessTestCase(unittest.TestCase):

    def testPlus(self):
        self.assertEquals(prim.plus(intl(1), intl(2), intl(3)), intl(6))

class PrimitiveFailureTestCase(unittest.TestCase):

    def testPlus(self):
        self.assertRaises(TypeError, prim.plus, intl(1), "two", intl(3))
