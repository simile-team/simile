# simile/error.py
"""
Custom error/exception types for the simile library.
"""

class ApiKeyNotSetError(Exception):
    pass

class AuthenticationError(Exception):
    pass

class RequestError(Exception):
    def __init__(self, message, status_code=None, response=None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response
