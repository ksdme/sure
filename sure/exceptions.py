"""
    @author ksdme
    Exception Classes for Sure
"""

class SureTypeError(Exception):
    """ type error """

    def __init__(self, msg=""):
        super(SureTypeError, self).__init__(msg)

class SureValueError(Exception):
    """ value error """

    def __init__(self, msg=""):
        super(SureValueError, self).__init__(msg)
