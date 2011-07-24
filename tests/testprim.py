import unittest

import prim

class PrimitiveSuccessTestCase(unittest.TestCase):

    def testPlus(self):
        self.assertEquals(prim.plus(1, 2, 3), 6)

class PrimitiveFailureTestCase(unittest.TestCase):

    def testPlus(self):
        self.assertRaises(TypeError, prim.plus, 1, "two", 3)
