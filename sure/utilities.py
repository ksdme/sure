"""
    @author ksdme
    Contains Utilities
"""
from sure.exceptions import SureTypeError

def u_resolve_fail(throws=False):
    """
        decides what to do when
        fail signal is returned
    """

    if throws is None:
        throws = False

    if throws:
        raise SureTypeError()
    else:
        return Consts.Fail

class ConstantValue(object):
    """ simply used to build refs """

    def __str__(self):
        return self.msg

    def __init__(self, msg):
        self.msg = msg

class Consts(object):
    """
        Constants,
        Enables reference checking
        instead of value comparison
    """

    # Used only in cases when a test fails
    Fail = ConstantValue("Failed")

    # Used to represent bool vals
    Truee = ConstantValue("True")
    Faalse = ConstantValue("False")

    @staticmethod
    def bool(val):
        """
            boolify into Truee's and Faalse's
            this helps to reference check
        """

        if val is False:
            return Consts.Faalse

        return Consts.Truee

    # Pass Signal
    Pass = ConstantValue("Passed")

    # Undefined yet
    Undefined = ConstantValue("Undefined")
