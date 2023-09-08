class V2VUserException(Exception):
    pass

class V2VInputError(V2VUserException): # base class for everything related to data input
    pass

class V2VConfigurationError(V2VUserException):
    pass
