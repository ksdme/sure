"""
    @author ksdme
    Available type decls and the base Type Class
"""
from sure.utilities import Consts
from sure.exceptions import SureTypeError

# TODO: find a better way to make type registry
# with the Type class

def u_condition_checker(frm, cond):
    """
        build a checker out of a condition
    """

    return Type(frm, cond)

def u_base_type(frm, typ):
    """
        utility to build basic instance
        type based checkers
    """

    lamda = lambda val: val if isinstance(val, typ) else Consts.Fail
    return u_condition_checker(frm, lamda)

# ----------------------------------------
# Primary Data Types
# ----------------------------------------
def integer(frm=None):
    """ chainable integer type checker """

    return u_base_type(frm, int)

def floating(frm=None):
    """ chainable float type checker """

    return u_base_type(frm, float)

def string(frm=None):
    """ chainable string type checker """

    return u_base_type(frm, str)

def klass(typ, frm=None):
    """ chainable class type checker """

    return u_base_type(frm, typ)

def null(frm=None):
    """ always returns None """

    lamda = lambda val: None
    return u_condition_checker(frm, lamda)

# ----------------------------------------
# Derived Data Types
# ----------------------------------------
def array(typ, frm=None):
    """
        checks if all the elements in the
        array are of the type 'typ'
    """

    def _internal(val):
        if not isinstance(val, list):
            return Consts.Fail

        for elm in val:
            if typ(val=elm) is Consts.Fail:
                return Consts.Fail

        return val

    return u_condition_checker(frm, _internal)

def accept(frm=None):
    """ accepts all """

    lamda = lambda val: val
    return u_condition_checker(frm, lamda)

# ----------------------------------------
# Property Checkers
# ----------------------------------------
def positive(frm=None):
    """ chainable integer type checker """

    lamda = lambda val: val if val > 0 else Consts.Fail
    return u_condition_checker(frm, lamda)

def length(rnge, frm):
    """
        checks for the length of the val,
        works with array type too, if rnge
        is a tuple it considers it as range
        the length should be in, else it
        considers the int as the min length
    """
    if isinstance(rnge, tuple) or isinstance(rnge, list):
        assert all(map(lambda l: isinstance(l, int), rnge))
    else:
        assert isinstance(rnge, int)

    def _internal(val):
        leng = len(val)
        if isinstance(rnge, tuple):
            if rnge[0] <= leng <= rnge[1]:
                return val
            else:
                return Consts.Fail
        else:
            return val if leng >= rnge else Consts.Fail

    return u_condition_checker(frm, _internal)

# ----------------------------------------
# Boolean Operations
# ----------------------------------------
def bool_or(*args, **kargs):
    """
        boolean or
        or between two types
    """

    # make sure we got frm
    frm = None
    try:
        frm = kargs["frm"]
    except KeyError:
        pass

    def _internal(val):
        for elm in args:
            if elm(val=val) is not Consts.Fail:
                return val

        return Consts.Fail

    return u_condition_checker(frm, _internal)

def bool_and(*args, **kargs):
    """
        boolean and
        and between two types
    """

    # make sure we got frm
    frm = None
    try:
        frm = kargs["frm"]
    except KeyError:
        pass

    def _internal(val):
        for elm in args:
            if elm(val=val) is Consts.Fail:
                return Consts.Fail

        return val

    return u_condition_checker(frm, _internal)

# ----------------------------------------
# Extras
# ----------------------------------------
def default(typ, default=None, frm=None):
    """ optional value """

    def _internal(val):
        if typ(val) is Consts.Fail:
            return default
        else:
            return val

    return u_condition_checker(frm, _internal)

def const(always, frm=None):
    """ always returns a const value """

    lamda = lambda val=None: always
    return u_condition_checker(frm, lamda)

def optional(typ, frm=None):
    """
        provides optional interfacting,
        basically an alias for default
    """

    return default(typ, Consts.Optional, frm)

def func(callble, frm=None):
    """
        provides an interface to use a
        custom function to build the type
    """

    assert isinstance(callble, callable)
    return u_condition_checker(frm, callble)
 
# ----------------------------------------
# Facilitate Fluent Interfacing
# ----------------------------------------
class BuiltInTypes(object):
    """ wraps up the builtin types """

    def integer(self):
        return integer(self)

    def floating(self):
        return floating(self)

    def string(self):
        return string(self)

    def klass(self, typ):
        return klass(typ, self)

    def null(self):
        return null(self)

    def array(self, typ):
        return array(typ, self)

    def accept(self):
        return accept(self)

    def bool_or(self, *args):
        return bool_or(*args, frm=self)

    def bool_and(self, *args):
        return bool_and(*args, frm=self)

    def default(self, typ, default=None):
        return default(typ, default, frm=self)

    def const(self, val):
        return const(val, frm=self)

    def optional(self, val):
        return optional(val, frm=self)

    def positive(self):
        return positive(self)

    def length(self, rnge):
        return length(rnge, self)

    def func(self, callble):
        return func(callble, frm=self)

class Type(BuiltInTypes):
    """
        Provides a basic class
        for type
    """

    def __init__(self, old=None, typ=None):
        """ clones from old or """

        self.reinit()

        if old is not None:
            self._type_q = list(old.type_q)

        if typ is not None:
            assert callable(typ)
            self.type_q.append(typ)

    def __call__(self, val):
        """ validates """

        for elm in self.type_q:
            val = elm(val=val)

            if val is Consts.Fail:
                return Consts.Fail

        return val

    def reinit(self):
        """ reinit object """

        self._type_q = []

    type_q = property(lambda self: self._type_q)
