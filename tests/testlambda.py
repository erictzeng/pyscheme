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
from env import GlobalEnv
import pyscheme

glob = GlobalEnv()

def pyscheme_eval(stmt):
    return pyscheme.make_list(stmt).car.eval(glob)

class LambdaNoArgsTestCase(unittest.TestCase):
    
    def testLambda(self):
        self.assertEquals(pyscheme.make_list("((lambda () 3))").car.eval(glob), intl(3))


class LambdaMultipleBodyStmtsTestCase(unittest.TestCase):
    
    def testLambda(self):
        self.assertEquals(pyscheme_eval("((lambda () 1 2 3))"), intl(3))
