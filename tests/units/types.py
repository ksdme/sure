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

    def test_flat_const(self):
        """ checks for the const type filter """

        self.assertEqual(const(None)(None), None)
        self.assertEqual(const("Hey")(None), "Hey")
        self.assertEqual(const(12345)(None), 12345)

        self.assertTrue(const(Consts.Fail)(None) is Consts.Fail)

    def test_flat_integer(self):
        """ check type returns and exceptions """

        typ = integer()
        self.assertEqual(typ(2), 2)
        self.assertTrue(typ([]) is Consts.Fail)
        self.assertTrue(typ("") is Consts.Fail)
        self.assertTrue(typ(2.5) is Consts.Fail)

    def test_flat_floating(self):
        """ floating type check"""

        typ = floating()
        self.assertEqual(typ(2.5), 2.5)
        self.assertTrue(typ(2) is Consts.Fail)
        self.assertTrue(typ("2.5") is Consts.Fail)

    def test_flat_string(self):
        """ strings checker """

        typ = string()
        self.assertEqual(typ(""), "")
        self.assertTrue(typ([]) is Consts.Fail)
        self.assertTrue(typ(123) is Consts.Fail)

    def test_flat_klass(self):
        """ klass instance testing """

        class _I1(object):
            pass

        class _I2(_I1):
            pass

        class _I3(object):
            pass

        sample1, sample2, sample3 = _I1(), _I2(), _I3()
        typ = klass(_I1)
        self.assertEqual(typ(sample1), sample1)
        self.assertEqual(typ(sample2), sample2)
        self.assertTrue(typ(sample3) is Consts.Fail)
        self.assertTrue(typ(123) is Consts.Fail)

    def test_flat_positive(self):
        """ ensure it is a positive number """

        typ = positive()
        self.assertEqual(typ(""), "")
        self.assertEqual(typ(2.5), 2.5)
        self.assertTrue(typ(-1) is Consts.Fail)

    def test_flat_array(self):
        """ tests for an array of values """

        typ = array(integer())
        self.assertTrue(typ(1) is Consts.Fail)
        self.assertTrue(typ([1, 2, "3"]) is Consts.Fail)
        self.assertEqual(typ([1, 2, 3]), [1, 2, 3])

    def tests_flat_accept(self):
        """ accept all """

        typ = accept()
        self.assertEqual(typ(1), 1)
        self.assertEqual(typ(None), None)
        self.assertEqual(typ(Consts.Fail), Consts.Fail)

    def test_flat_null(self):
        """ null """

        typ = null()
        self.assertEqual(typ(""), None)
        self.assertEqual(typ(12), None)
        self.assertEqual(typ([]), None)

    def test_flat_bool_or(self):
        """ test or """

        typ = bool_or(positive(integer()), string())
        self.assertEqual(typ(1), 1)
        self.assertEqual(typ(""), "")
        self.assertTrue(typ(-1) is Consts.Fail)
        self.assertTrue(typ(1.5) is Consts.Fail)
        self.assertTrue(typ([1]) is Consts.Fail)

    def test_flat_bool_and(self):
        """ test and """

        typ = bool_and(positive(), integer())
        self.assertEqual(typ(1), 1)
        self.assertTrue(typ("") is Consts.Fail)
        self.assertTrue(typ(-1) is Consts.Fail)
        self.assertTrue(typ(1.5) is Consts.Fail)
        self.assertTrue(typ([1]) is Consts.Fail)

    def test_nested_integer(self):
        """ tests nested integer() """

        typ = integer(positive())
        self.assertEqual(typ(1), 1)
        self.assertTrue(typ("") is Consts.Fail)
        self.assertTrue(typ(-1) is Consts.Fail)

        typ = integer().positive()
        self.assertEqual(typ(1), 1)
        self.assertTrue(typ("") is Consts.Fail)
        self.assertTrue(typ(-1) is Consts.Fail)

    def test_nested_floating(self):
        """ simply tests a for nesting consistency """

        typ = floating(positive())
        self.assertEqual(typ(10.0), 10.0)
        self.assertTrue(typ("") is Consts.Fail)
        self.assertTrue(typ(10) is Consts.Fail)
        self.assertTrue(typ(-10.0) is Consts.Fail)

        typ = floating().positive()
        self.assertEqual(typ(10.0), 10.0)
        self.assertTrue(typ("") is Consts.Fail)
        self.assertTrue(typ(10) is Consts.Fail)
        self.assertTrue(typ(-10.0) is Consts.Fail)

    def test_nested_klass(self):
        """ klass's nested behaviour """

        typ = klass(int, positive())
        self.assertEqual(typ(15), 15)
        self.assertTrue(typ("") is Consts.Fail)
        self.assertTrue(typ(-10) is Consts.Fail)

    def test_nested_positive(self):
        """ test class positive """

        typ = positive(integer())
        self.assertEqual(typ(10), 10)
        self.assertTrue(typ(-10) is Consts.Fail)
        self.assertTrue(typ(10.0) is Consts.Fail)
        self.assertTrue(typ("") is Consts.Fail)

        typ = positive().integer()
        self.assertEqual(typ(10), 10)
        self.assertTrue(typ(-10) is Consts.Fail)
        self.assertTrue(typ(10.0) is Consts.Fail)
        self.assertTrue(typ("") is Consts.Fail)

    def test_nested_array(self):
        """ test array nested """

        typ = array(integer(), accept())
        self.assertEqual(typ([1, 2, 3]), [1, 2, 3])
        self.assertTrue(typ(1) is Consts.Fail)

        typ = array(integer()).accept()
        self.assertEqual(typ([1, 2, 3]), [1, 2, 3])
        self.assertTrue(typ(1) is Consts.Fail)

    def test_flat_dictionary(self):
        """ test dictionary() """

        typ = dictionary(string(), integer())
        self.assertEqual(typ({ "a": 1 }), { "a": 1 })
        self.assertEqual(typ({ "a": 1, "b": 2 }), { "a": 1, "b": 2 })
        self.assertTrue(typ({ 0: 1 }) is Consts.Fail)
        self.assertTrue(typ([ 0, 1 ]) is Consts.Fail)
        self.assertTrue(typ({ "0": "1" }) is Consts.Fail)
