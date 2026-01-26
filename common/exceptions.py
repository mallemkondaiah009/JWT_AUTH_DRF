from rest_framework.exceptions import APIException

class UserAlreadyExists(APIException):
    status_code = 401
    default_detail = "Username or email already exists"