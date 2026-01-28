# accounts/authentication.py
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.conf import settings
from accounts.models import User

class JWTauth(JWTAuthentication):
    """
    Custom JWT auth that reads token from request.data['access_token']
    """
    def authenticate(self, request):
        # Get token from POST body or GET query params
        raw_token = request.data.get('access_token')
        
        if not raw_token:
            return None  # no token provided

        try:
            validated_token = self.get_validated_token(raw_token)

            # Extract user_id
            user_id = validated_token[settings.SIMPLE_JWT['USER_ID_CLAIM']]

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                raise AuthenticationFailed('User not found', code='user_not_found')

            return user, validated_token

        except (InvalidToken, TokenError):
            raise AuthenticationFailed('Invalid or expired token')
