"""
    @author ksdme
    Available type decls
"""
from sure.utilities import Consts
from sure.exceptions import SureTypeError

# global value
class SureConfig:
    """ holds config values """

    THROWS = True

def u_resolve_fail(throws=False):
    """
        decides what to do when a
        fail signal is returned
    """

    if throws is None:
        throws = SureConfig.THROWS

    if throws:
        raise SureTypeError()
    else:
        return Consts.Fail

def u_resolve_nested(base, nested=None):
    """
        remakes a kiln function to
        ensure it can be nesteded
    """

    if callable(nested):
        return lambda val: base()(val=nested(val=val))
    else:
        return False

def u_base_type(condition, typ_func, nested=None, throws=None):
    """
        ensures that the flowing data is
        of type typ
    """

    val = u_resolve_nested(typ_func, nested)
    if val is not False:
        return val

    def _internal(val):
        if not condition(val):
            return u_resolve_fail(throws)
        else:
            return val

    return _internal

def const(val):
    """ simply return a constant val """

    return lambda v=None: val

def integer(nested=None, throws=None):
    """ ensure it is an int """

    condition = lambda val: isinstance(val, int)
    return u_base_type(condition, integer, nested, throws)

def floating(nested=None, throws=None):
    """ ensure it is a float """

    condition = lambda val: isinstance(val, float)
    return u_base_type(condition, floating, nested, throws)

#! no test unit for nested behaviour
def string(nested=None, throws=None):
    """ ensure it is a float """

    condition = lambda val: isinstance(val, str)
    return u_base_type(condition, string, nested, throws)

def klass(typ, nested=None, throws=None):
    """ ensures val is an instance of klass """

    condition = lambda val: isinstance(val, typ)
    recall = lambda nested=None, throws=None: klass(typ, nested, throws)
    return u_base_type(condition, recall, nested, throws)

def positive(nested=None, throws=None):
    """ ensure it is a float """

    def _condition(val):
        try:
            if float(val) > 0:
                return val
            else:
                return False
        except:
            return False

    return u_base_type(_condition, positive, nested, throws)
