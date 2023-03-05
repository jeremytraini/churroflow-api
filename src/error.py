from fastapi import HTTPException

class AuthenticationError(HTTPException):
    status_code = 403
    detail = 'You are unauthorised to access this resource'

class InputError(HTTPException):
    status_code = 400
    detail = 'The input you have provided is invalid'
