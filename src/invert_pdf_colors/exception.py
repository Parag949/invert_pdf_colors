import sys


class InvertPDFColorsException(Exception):
    """Custom exception with optional system context."""

    def __init__(self, message: str, *args, **kwargs):
        super().__init__(message, *args)
        self.message = message
        self.exc_info = sys.exc_info()

    def __str__(self) -> str:
        return f"InvertPDFColorsException: {self.message}"
