from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.response import Response
from rest_framework import status

class UserAlreadyExists(APIException):
    status_code = 401
    default_detail = "Username or email already exists"


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    # JWT token errors
    if isinstance(exc, TokenError):
        return Response(
            {
                "success": False,
                "errors": "Invalid or expired token"
            },
            status=status.HTTP_401_UNAUTHORIZED
        )

    if response is not None:
        return Response(
            {
                "success": False,
                "errors": response.data
            },
            status=response.status_code
        )

    return Response(
        {
            "success": False,
            "errors": "Internal Server Error"
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )

