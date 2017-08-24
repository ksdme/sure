"""
    @author ksdme
    tests the sure.builder module
"""
from unittest import TestCase
from sure.types import integer, string, positive
from sure.builder import prop, nested_prop, nested, TypedModel
from sure.exceptions import SureTypeError, SureValueError, ModelFreezed

class TestBuilder(TestCase):
    """ tests builder """

    def test_flat_builder(self):
        """ builder class """

        class Sample(TypedModel):
            name = prop(string())
            serial = prop(integer().positive())

        sample = Sample()
        sample.name = "@ksdme"
        sample.serial = 250145

        self.assertEqual(sample.name, "@ksdme")
        self.assertEqual(sample.serial, 250145)

        with self.assertRaises(SureTypeError):
            sample.name = 123456

        with self.assertRaises(SureTypeError):
            sample.serial = -15014

    def test_nested_builder(self):
        """ tests nested builder """

        class Human(TypedModel):
            family = nested_prop({
                "father": nested({
                    "name": string().length(5),
                    "age": integer().positive()}),

                "mother": nested({
                    "name": string().length(5),
                    "age": integer().positive(),
                    "family": nested({
                        "father": string()
                    })})
            })

        mine = Human()

        mine.family.father = {
            "name": "Kilari",
            "age": 25
        }

        mine.family.mother = {
            "family": {
                "father": "dad"
            }
        }

        self.assertEqual(mine.family.father.age, 25)
        self.assertEqual(mine.family.mother.family.father, "dad")

        with self.assertRaises(SureTypeError):
            mine.family.father.age = "20"

        with self.assertRaises(SureTypeError):
            mine.family.father = {
                "age": "20"
            }

    def test_nested_constr_builder(self):
        """ simply test the basic cons builder """

        class Sample(TypedModel):
            serial = prop(integer())
            name = nested_prop({
                "first": string(),
                "last": string(),

                "dob": {
                    "date": integer().positive(),
                    "mont": integer(),
                    "year": integer()
                }
            }, False)

        values = {
            "name.first":   "Kilari",
            "name.last":    "Teja",
            "name.dob.date": 10
        }

        sample = Sample(values, serial=123)
        self.assertEqual(sample.serial, 123)
        self.assertEqual(sample.name.first, "Kilari")
        self.assertEqual(sample.name.dob.date, 10)

        with self.assertRaises(SureValueError):
            sample.name.dob.mont

        with self.assertRaises(ModelFreezed):
            sample.names = 50

        sample.name.dob.date = 20

