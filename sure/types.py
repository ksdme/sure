"""
    @author ksdme
    Available type decls
"""
from sure.utilities import u_resolve_fail, Consts

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
        ensures that the flowing data
        is of type typ
    """

    val = u_resolve_nested(typ_func, nested)
    if val is not False:
        return val

    def _internal(val):
        flag = condition(val)
        if flag is Consts.Faalse:
            return u_resolve_fail(throws)
        else:
            return val

    return _internal

def const(val):
    """ simply return a constant val """

    return lambda v=None: val

def integer(nested=None, throws=None):
    """ ensure it is an int """

    condition = lambda val: Consts.bool(isinstance(val, int))
    return u_base_type(condition, integer, nested, throws)

def floating(nested=None, throws=None):
    """ ensure it is a float """

    condition = lambda val: Consts.bool(isinstance(val, float))
    return u_base_type(condition, floating, nested, throws)

#! no test unit for nested behaviour
def string(nested=None, throws=None):
    """ ensure it is a float """

    condition = lambda val: Consts.bool(isinstance(val, str))
    return u_base_type(condition, string, nested, throws)

def klass(typ, nested=None, throws=None):
    """ ensures val is an instance of klass """

    condition = lambda val: Consts.bool(isinstance(val, typ))
    recall = lambda nested=None, throws=None: klass(typ, nested, throws)
    return u_base_type(condition, recall, nested, throws)

def positive(nested=None, throws=None):
    """ ensure it is a float """

    def _condition(val):
        try:
            if float(val) > 0:
                return val
            else:
                return Consts.Faalse
        except:
            return Consts.Faalse

    return u_base_type(_condition, positive, nested, throws)

def array(typ, nested=None, throws=None):
    """ makes sure that it is a single typed array """

    def _internal(val):
        if not (isinstance(val, list) or isinstance(val, tuple)):
            return Consts.Faalse

        flag = all(map(lambda l: typ(l) is not Consts.Fail, val))
        return val if flag else Consts.Faalse

    recall = lambda nested=None, throws=None: array(typ, nested, throws)
    return u_base_type(_internal, recall, nested, throws)

def accept_all(nested=None, throws=None):
    """ everything I see or feel is good enough """

    return u_base_type(lambda val: val, accept_all, nested, throws)

def null(nested=None, throws=None):
    """ returns None no matter what """

    return lambda val: None

def bool_or(*args):
    """ as simple as that sounds """

    def _internal(val):
        for arg in args:
            if arg(val) is not Consts.Fail:
                return val

        return Consts.Fail

    return _internal

def bool_and(*args):
    """ bool and """

    def _internal(val):
        for arg in args:
            if arg(val) is Consts.Fail:
                return Consts.Fail

        return val

    return _internal
