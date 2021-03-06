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

class ModelFreezed(Exception):
    """ model has been freezed """

    def __init__(self, msg=""):
        super(ModelFreezed, self).__init__(msg)

class MalformedModel(Exception):
    """
        valued model musn't have multiple attributes
    """

    def __init__(self, msg=""):
        super(MalformedModel, self).__init__(msg)
