class SchemeError(Exception):
    pass

# Unbound variable
class UnboundVariableError(SchemeError):
    def __init__(self, var):
        self.msg = "Unbound variable {0}".format(var)

# IllegalArgumentErrors
class IllegalArgumentError(SchemeError):
    pass

# Bad number of arguments
class ArgumentCountError(IllegalArgumentError):
    def __init__(self, function, expected, given):
        self.msg = "Bad number of arguments: {0} takes {1} arguments ({2} given)".format(function, given, expected)

# Wrong type of argument
class WrongArgumentType(IllegalArgumentError):
    def __init__(self, function, expected, given):
        self.msg = "Wrong type of argument for {0}: Expected {1} ({2} given)".format(function, expected, given)