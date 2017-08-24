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
        return "Const: " + str(self.msg)

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

    # simple optional flag
    Optional = ConstantValue("Opt")

    # Undefined yet
    Undefined = ConstantValue("Undefined")
