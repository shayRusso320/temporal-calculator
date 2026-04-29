"""Custom exceptions for the distributed calculator system."""


class CalculatorException(Exception):
    """Base exception for calculator errors."""

    pass


class ParseError(CalculatorException):
    """Raised when expression parsing fails."""

    pass


class DivisionByZeroError(CalculatorException):
    """Raised when attempting to divide by zero."""

    pass
