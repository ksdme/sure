"""
    @author ksdme
    this module holds functions to build the
    actual data type models using types module
"""
from time import time
from random import randrange
from sure.utilities import Consts, u_resolve_fail
from sure.exceptions import SureTypeError, TypeDefinitionError, SureValueError

class StaticModel(object):
    """
        parent class for all static type
        holders
    """

    def __init__(self, deep=None, **kargs):

        # set unnested attributes
        for name, val in kargs.iteritems():
            setattr(self, name, val)

        # set deep internal stuff
        for name, val in deep:
            name, context = name.strip().split("."), self
            for elm in name[:-1]:
                context = getattr(context, elm)

            setattr(context, name[-1], val)

def _gen_random_name():
    """
        generates random name
    """

    val_name = str(randrange(10000))
    val_name += "{0:.20f}".format(time()).replace(".", "")
    val_name = "_var" + val_name

    return val_name

def gen_prop_getter(val_name, setter, throws):
    """
        generates a getter function for a class
        propety going by val_name, evals by checking
        if it undefined yet and if it is, tries setting
        it with an undefined just to see that it aint a
        opt() type data struct
    """

    def _internal(self):
        attr = Consts.Undefined
        try:
            attr = getattr(self, val_name)
        except AttributeError:
            if throws:
                raise SureValueError()

            setattr(self, val_name, Consts.Undefined)


        if attr is Consts.Undefined:
            try:
                setter(self, Consts.Undefined)
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
            return u_resolve_fail(throws)

    return _internal

def prop(typ, throws=True):
    """
        generates a random name for the property
        and sets up the setter and getter
    """
    val_name = _gen_random_name()

    setter = gen_prop_setter(val_name, typ, throws)
    getter = gen_prop_getter(val_name, setter, throws)

    return property(getter, setter)

def gen_nested_prop_getter(val_name, throws, klass):
    """
        generates a nested property getter, it
        actually returns an _Internal object
    """

    def _internal(self):
        try:
            getattr(self, val_name)
        except AttributeError:
            setattr(self, val_name, klass())

        return getattr(self, val_name)

    return _internal

def gen_nested_prop_setter(val_name, throws, klass):
    """
        generates a nested property setter,
        it basically linearly tests and assigns
    """

    def _internal(self, value):
        assert isinstance(value, dict)

        try:
            getattr(self, val_name)
        except AttributeError:
            setattr(self, val_name, klass())

        this = getattr(self, val_name)
        for elm, val in value.iteritems():
            try:
                setattr(this, elm, val)
            except SureTypeError():
                setattr(self, val_name, this)

                if throws:
                    return Consts.Fail
                else:
                    raise SureTypeError()

    return _internal

# nested prop indicates nested stuff
def nested_prop(nestd, throws=True):
    """
        helps build a nested property map
    """
    assert isinstance(nestd, dict)
    val_name = _gen_random_name()

    # generate a struct class
    class _InternalStruct(object): pass

    for elm, typ in nestd.iteritems():
        if isinstance(typ, property):
            setattr(_InternalStruct, elm, typ)
        else:
            assert callable(typ), "TypeDefinitionError"
            setattr(_InternalStruct, elm, prop(typ, True))

    setter = gen_nested_prop_setter(val_name, throws, _InternalStruct)
    getter = gen_nested_prop_getter(val_name, throws, _InternalStruct)
    return property(getter, setter)

def nested(nestd, throws=True):
    """
        helps you build a nested inside a nested
        prop, it basically acts liek that too
    """

    return nested_prop(nestd, throws)
