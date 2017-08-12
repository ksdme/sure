"""
    @author ksdme
    Available type decls
"""
from sure.utilities import Consts
from sure.exceptions import SureTypeError

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
# Facilitate Fluent Interfacing
# ----------------------------------------
class PrimaryTypes(object):
    """ wraps up the primary types """

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

class DerivedTypes(object):
    """ wraps derived types """

    def array(self, typ):
        return array(typ, self)

    def accept(self):
        return accept(self)

class PropertyCheckers(object):
    """ wraps property checkers """

    def positive(self):
        return positive(self)

    def length(self, rnge):
        return length(rnge, self)

class BooleanOps(object):
    """ wraps boolean ops """

    def bool_or(self, *args):
        return bool_or(*args, frm=self)

    def bool_and(self, *args):
        return bool_and(*args, frm=self)

class Type(PrimaryTypes,
           DerivedTypes,
           PropertyCheckers,
           BooleanOps):
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
