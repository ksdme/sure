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

class TypeDefinitionError(Exception):
    """ type error """

    def __init__(self, msg=""):
        super(TypeDefinitionError, self).__init__(msg)

class RequiredValueMissing(Exception):
    """ missing a value that is not opt """

    def __init__(self, msg=""):
        super(RequiredValueMissing, self).__init__(msg)
