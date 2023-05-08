from fastapi import HTTPException
from starlette import status


class DiscordBotIsNotInit(Exception):
    pass


class UnknownLink(Exception):
    pass


class UserEmailExists(HTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "User with this email is exists. Try again with other email"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class PasswordMismatch(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Password mismatch"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class IncorrectFormData(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect username or password"
    headers = {"WWW-Authenticate": "Bearer"}

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail,
                         headers=self.headers)


class Unauthorized(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Could not validate credentials"
    headers = {"WWW-Authenticate": "Bearer"}

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail,
                         headers=self.headers)
