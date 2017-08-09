"""
    @author ksdme
    Contains Utilities
"""

class _DUMB(object):
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
    Fail = _DUMB("Failed")

    # Used to represent bool vals
    Faalse = _DUMB("False")
    Truee = _DUMB("True")

    @staticmethod
    def bool(val):
        if val is False:
            return Consts.Faalse

        return Consts.Truee

    # Pass Signal
    Pass = _DUMB("Passed")

    # Undefined yet
    Undefined = _DUMB("Undefined")
