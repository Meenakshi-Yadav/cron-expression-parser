# General parser error for invalid cron strings
class ParserError(Exception):
    def __init__(self, message = "Invalid format."):
        super().__init__(message)

# Error raised when an individual field is invalid 
class InvalidField(ParserError):
    def __init__(self, message):
        super().__init__(message)
