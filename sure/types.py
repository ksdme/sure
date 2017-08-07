"""
    @author ksdme
    Available type decls
"""
from sure.utilities import Consts
from sure.exceptions import SureTypeError

# global value
THROWS = True

def u_resolve_fail(throws=False):
    """
        decides what to do when a
        fail signal is returned
    """

    if throws:
        raise SureTypeError()
    else:
        return Consts.Fail

def u_resolve_digest(base, digest=None):
    """
        remakes a kiln function to
        ensure it can be nested
    """

    if callable(digest):
        return lambda val: base()(val=digest(val=val))
    else:
        return False

def u_base_type(condition, typ_func, digest=None, throws=THROWS):
    """
        ensures that the flowing data is
        of type typ
    """

    val = u_resolve_digest(typ_func, digest)
    if val is not False:
        return val

    def _internal(val):
        if condition(val):
            u_resolve_fail(throws)
        else:
            return val

    return _internal

def integer(digest=None, throws=THROWS):
    """ ensure it is an int """

    condition = lambda val: isinstance(val, int)
    return u_base_type(condition, integer, digest, throws)

def floating(digest=None, throws=THROWS):
    """ ensure it is a float """

    condition = lambda val: isinstance(val, float)
    return u_base_type(condition, floating, digest, throws)

def string(digest=None, throws=THROWS):
    """ ensure it is a float """

    condition = lambda val: isinstance(val, str)
    return u_base_type(condition, string, digest, throws)

def klass(typ, digest=None, throws=THROWS):
    """ ensures val is an instance of klass """

    condition = lambda val: isinstance(val, typ)
    recall = lambda digest, throws: klass(typ, digest, throws)
    return u_base_type(condition, recall, digest, throws)

def positive(digest=None, throws=THROWS):
    """ ensure it is a float """

    condition = lambda val: float(val) > 0
    return u_base_type(condition, positive, digest, throws)
