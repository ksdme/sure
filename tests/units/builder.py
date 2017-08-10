"""
    @author ksdme
    tests the sure.builder module
"""
from unittest import TestCase
from sure.builder import prop
from sure.exceptions import SureTypeError
from sure.types import integer, string, positive

class TestBuilder(TestCase):
    """ tests builder """

    def test_builder(self):
        """ builder class """

        class Sample(object):
            name = prop(string())
            serial = prop(integer(positive()))

        sample = Sample()
        sample.name = "@ksdme"
        sample.serial = 250145

        self.assertEqual(sample.name, "@ksdme")
        self.assertEqual(sample.serial, 250145)

        with self.assertRaises(SureTypeError):
            sample.name = 123456

        with self.assertRaises(SureTypeError):
            sample.serial = -15014
