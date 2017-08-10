"""
    @author ksdme
    this module holds functions to build the
    actual data type models using types module
"""
from time import time
from random import randrange
from sure.utilities import Consts
from sure.types import u_resolve_fail
from sure.exceptions import SureTypeError

# simple global config
class Config:

    # maximum value of a random salt
    # used during generating val_name
    MaxSalt = 100000

def gen_prop_getter(val_name, setter):
    """
        generates a getter function for a class
        propety going by val_name, evals by checking
        if it undefined yet and if it is, tries setting
        it with an undefined just to see that it aint a
        opt() type data struct
    """

    def _internal(self):
        try:
            attr = getattr(self, val_name)
        except AttributeError:
            return Consts.Undefined

        if attr is Consts.Undefined:
            try:
                setter(Consts.Undefined)
            except SureTypeError:
                pass

        return getattr(self, val_name)

    return _internal

def gen_prop_setter(val_name, typ, throws):
    """
        generates a setter function for a class
        property going by val_name, ensures that
        the value meets criteria else doesn't
        change it
    """

    def _internal(self, value):
        value = typ(value)
        if value is not Consts.Fail:
            setattr(self, val_name, value)
        elif value is Consts.Fail:
            u_resolve_fail(throws)

    return _internal

def prop(typ, throws=True):
    """
        generates a random name for the property
        and sets up the setter and getter
    """
    val_name = str(randrange(Config.MaxSalt))
    val_name += "{0:.20f}".format(time()).replace(".", "")
    val_name = "_var" + val_name

    setter = gen_prop_setter(val_name, typ, throws)
    getter = gen_prop_getter(val_name, setter)

    return property(getter, setter)
