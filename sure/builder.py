"""
    @author ksdme
    this module holds functions to build the
    actual data type models using types module
"""
from time import time
from sure.types import Type
from random import randrange
from sure.utilities import Consts, u_resolve_fail
from sure.exceptions import SureTypeError, SureValueError
from sure.exceptions import ModelFreezed, RequiredValueMissing

# we need to have some kind of a prefix
# to dynamically added variables, so it'll
# be __var
DYNAMIC_PROPS_PREFIX = "__var"

class TypedModel(object):
    """
        parent class for all static type
        holders
    """

    # we'll use only the instance's
    # copy of __freezed though
    __freezed = False

    def __setattr__(self, key, val):

        if key.find(DYNAMIC_PROPS_PREFIX) != -1 or key in dir(self):
            object.__setattr__(self, key, val)

        elif self.__freezed:
            raise ModelFreezed()

        else:
            object.__setattr__(self, key, val)

    def __init__(self, deep={}, **kargs):

        # you can also ignore prop() usage
        # this part rebuilds vals using props
        self_class = self.__class__
        if self_class.__doc__ is not None:
            self_doc = self_class.__doc__.strip()
            if self_doc.startswith("@typed"):
                for elm in dir(self_class):
                    if elm.startswith("_"):
                        continue

                    val = getattr(self_class, elm)
                    if not isinstance(val, property):
                        if isinstance(val, Type) or isinstance(val, dict):
                            setattr(self_class, elm, prop(val, True))

        # set unnested attributes
        for name, val in kargs.iteritems():
            setattr(self, name, val)

        # set deep internal stuff
        for name, val in deep.iteritems():
            name, context = name.strip().split("."), self
            for elm in name[:-1]:
                context = getattr(context, elm)

            setattr(context, name[-1], val)

        # free the hell outta it
        self._freeze()

    # freezing function
    def _freeze(self):
        self.__freezed = True

    def __call__(self):
        """
            introspects and produce the struct
            used to json'ify or xml'ify
        """

        struct_holder = {}

        elms = filter(
            lambda self: not self.startswith("_"), dir(self))

        """
            this is certainly interesting,
            you first find all the public attributes via introspection
            and then 'get' all of them, if any of them raises an ValueErr
            then it indicates that it wasn't instantiated yet, so its always
            possible that the one left out was optional field, so it tries to
            set it to Undefined, Optional fields silently discard the value f
            it fails and instead give it an optional value, so they have no means
            of feedback, anyway, it tests in cases of nested stuff and calls the 
            internal struct holder to submit it struct. Also this thus supports
            using other TypedModel's as an nested property
        """
        for elm in elms:
            prop_val = Consts.Undefined
            
            try:
                prop_val = getattr(self, elm)
            except SureValueError:

                """
                    test if it is an optional field,
                    also test it again for its optional'ness
                    but this time with Const.Optional value
                """
                try:
                    setattr(self, elm, Consts.Undefined)
                except SureTypeError:
                    raise RequiredValueMissing()

                continue

            if prop_val is Consts.Optional:
                pass
            elif isinstance(prop_val, TypedModel):
                struct_holder[elm] = prop_val()
            else:
                struct_holder[elm] = prop_val

        return struct_holder

    def __str__(self):
        """ alias for __call__ """

        return str(self())

class _InternalTypedModel(TypedModel):

    def __init__(self):
        super(_InternalTypedModel, self).__init__()

def _gen_random_name():
    """
        generates random name
    """

    val_name = str(randrange(10000))
    val_name += "{0:.20f}".format(time()).replace(".", "")
    val_name = DYNAMIC_PROPS_PREFIX + val_name

    return val_name

def gen_prop_getter(val_name, setter, throws):
    """
        generates a getter function for a class
        propety going by val_name, it only knows
        if the value has atleast been set once or
        if it hasn't been instantiated yet
    """

    def _internal(self):
        try:
            getattr(self, val_name)
        except AttributeError:
            if throws:
                raise SureValueError()

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
    if isinstance(typ, dict):
        return nested_prop(typ, throws)

    val_name = _gen_random_name()

    setter = gen_prop_setter(val_name, typ, throws)
    getter = gen_prop_getter(val_name, setter, throws)

    return property(getter, setter)

# throws is for consistency
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

    # generate a internal model class
    class _InternalStruct(_InternalTypedModel):
        pass

    for elm, typ in nestd.iteritems():
        if isinstance(typ, property):
            setattr(_InternalStruct, elm, typ)
        elif isinstance(typ, dict):
            setattr(_InternalStruct, elm, nested(typ))
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
