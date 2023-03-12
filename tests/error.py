from fastapi.exceptions import HTTPException

class AccessError(HTTPException):
    code = 403
    message = 'No message specified'

class InputError(HTTPException):
    code = 400
    message = 'No message specified'

class AuthError(HTTPException):
    code = 401
    message = 'No message specified'
