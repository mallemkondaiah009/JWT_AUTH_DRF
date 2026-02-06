# accounts/authentication.py

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.conf import settings
from accounts.models import User

class JWTauth(JWTAuthentication):
    """
    JWT auth for custom User model using Authorization header
    """

    def authenticate(self, request):
        header = self.get_header(request)

        if header is None:
            return None

        raw_token = self.get_raw_token(header)

        if raw_token is None:
            return None

        try:
            validated_token = self.get_validated_token(raw_token)

            user_id = validated_token[settings.SIMPLE_JWT["USER_ID_CLAIM"]]

            try:
                user = User.objects.get(id=user_id, is_active=True)
            except User.DoesNotExist:
                raise AuthenticationFailed("User not found")

            return user, validated_token

        except (InvalidToken, TokenError):
            raise AuthenticationFailed("Invalid or expired token")
