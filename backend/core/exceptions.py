class GuardSQLException(Exception):
    pass

class ValidationError(GuardSQLException):
    pass

class ExecutionError(GuardSQLException):
    pass

class LLMError(GuardSQLException):
    pass

class AuthenticationError(GuardSQLException):
    pass
