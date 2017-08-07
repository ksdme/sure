"""
    @author ksdme
    Exception Classes for Sure
"""

class SureTypeError(Exception):
    """ Sure TypeError """

    def __init__(self, msg=""):
        super(SureTypeError, self).__init__(msg)
