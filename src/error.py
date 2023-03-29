from fastapi.exceptions import HTTPException

class InputError(HTTPException):
    status_code = 400
    detail = 'The input you have provided is invalid'

class TokenError(HTTPException):
    status_code = 402
    detail = 'The token is invalid'

class NotFoundError(HTTPException):
    status_code = 404
    detail = 'Input provided cannot be found'

class InternalServerError(HTTPException):
    status_code = 500
    detail = 'An internal server error occured'