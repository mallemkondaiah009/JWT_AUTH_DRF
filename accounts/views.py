from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from passlib.context import CryptContext
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.tokens import RefreshToken
import os
from dotenv import load_dotenv
from datetime import timedelta

from .models import User
from .serializers import RegisterSerializer, LoginSerializer, LoginResponseSerializer, RegisterSerializerResponse

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
        

