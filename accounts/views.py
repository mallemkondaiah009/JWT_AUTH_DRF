from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from passlib.context import CryptContext
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import IsAuthenticated
import os
from dotenv import load_dotenv
from datetime import timedelta
from django.conf import settings
from utils.jwt_check import JWTauth

from .models import User
from .serializers import RegisterSerializer, LoginSerializer, LoginResponseSerializer, RegisterSerializerResponse,UserUpdateSerializer

load_dotenv()

refresh_days = int(os.getenv("REFRESH_TOKEN_LIFETIME_DAYS", 10))
max_age_seconds = int(timedelta(days=refresh_days).total_seconds())

pwd_context = CryptContext(schemes=['argon2'], deprecated='auto')


class UserRegistration(APIView):

    serializer_class = RegisterSerializer

    @extend_schema(
        request=RegisterSerializer,
        responses={201: RegisterSerializerResponse},
        description="Register a new user. Returns user data without password."
    )

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "data":serializer.data,
                    "message":"User Registered Successfully"
                },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
    def get(self, request):
        user = User.objects.all()
        serializer = RegisterSerializer(user, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK

        )

class UserLogin(APIView):

    @extend_schema(
    request=LoginSerializer,
    responses={200: LoginResponseSerializer},
    description="Login using your existing email and password")

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        response = Response(
                    {
                        'message': 'Login Successful',
                        'access_token': str(refresh.access_token)
                    },
                    status=status.HTTP_200_OK
                )
        response.set_cookie(
                    key='refresh_token',
                    value=str(refresh),
                    httponly=True,
                    secure=True,
                    samesite='Lax',
                    max_age=max_age_seconds,
                    path='/'
                )
        return response
    
class AccessTokenRefresh(APIView):
    
    def post(self,request):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response(
                {'detail': 'Refresh token not found'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        try:
            refresh = RefreshToken(refresh_token)
            access = refresh.access_token

            if settings.SIMPLE_JWT.get('ROTATE_REFRESH_TOKENS'):
                refresh.set_jti()
                refresh.set_exp()

            response = Response(
                {
                    'access_token': str(access)
                },
                status=status.HTTP_200_OK
            )

            # update refresh cookie if rotated
            response.set_cookie(
                key="refresh_token",
                value=str(refresh),
                httponly=True,
                secure=True,
                samesite="Lax",
                max_age=max_age_seconds,
                path='/'
            )

            return response

        except TokenError:
            return Response(
                {"detail": "Invalid or expired refresh token"},
                status=status.HTTP_401_UNAUTHORIZED
            )

class UserProfile(APIView):
    authentication_classes = [JWTauth] 

    def get(self, request):
        user = request.user 
        return Response({
            "username": user.username,
            "email": user.email,
            "created_at": user.created_at
        }
        )
    
class UserUpdate(APIView):
    authentication_classes = [JWTauth]

    def patch(self, request):
        user = request.user
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request):
        user = request.user
        user.delete()
        

