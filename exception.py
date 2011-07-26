class SchemeError(Exception):
    pass

# Unbound variable
class UnboundVariableError(SchemeError):
    def __init__(self, var):
        self.msg = "Unbound variable {0}".format(var)

# IllegalArgumentErrors
class IllegalArgumentError(SchemeError):
    pass

# Bad number of parameters
class BadNumberOfParameters(SchemeError):
    def __init__(self, call):
        self.msg = "Bad number of parameters: {0}".format(call)

# Wrong type of argument
class WrongArgumentType(SchemeError):
    def __init__(self, function, arg):
        self.msg = "{0}: wrong type of argument: {1}".format(function, arg)
