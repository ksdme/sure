"""
    @author ksdme
    type system unit test
"""
import unittest
from sure.types import *
from sure.utilities import Consts
from sure.exceptions import SureTypeError

class TestTypeSystem(unittest.TestCase):
    """ TestTypeSystem """

    def setUp(self):
        SureConfig.THROWS = False

    def test_flat_integer(self):
        """ check type returns and exceptions """
        typ = integer()
        self.assertEqual(typ(2), 2)
        self.assertEqual(typ([]), Consts.Fail)
        self.assertEqual(typ(""), Consts.Fail)
        self.assertEqual(typ(2.5), Consts.Fail)

        typ = integer(throws=True)
        self.assertEqual(typ(2), 2)
        with self.assertRaises(SureTypeError):
            typ(2.5)

    def test_flat_positive(self):
        """ ensure it is a positive number """
        typ = positive()
        self.assertEqual(typ(2.5), 2.5)
        self.assertEqual(typ(-1), Consts.Fail)
        self.assertEqual(typ(""), Consts.Fail)

    def test_nested_integer(self):
        """ tests nested integer() """
        typ = integer(positive())
        self.assertEqual(typ(1), 1)
        self.assertEqual(typ(""), Consts.Fail)
        self.assertEqual(typ(-1), Consts.Fail)
