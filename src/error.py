from fastapi.exceptions import HTTPException

class AuthenticationError(HTTPException):
    status_code = 403
    detail = 'You are unauthorised to access this resource'

class InputError(HTTPException):
    status_code = 400
    detail = 'The input you have provided is invalid'

class AccessError(HTTPException):
    code = 403
    message = 'No message specified'

class AuthError(HTTPException):
    code = 401
    message = 'No message specified'
