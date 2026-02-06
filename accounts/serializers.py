from rest_framework.serializers import ModelSerializer, ValidationError
from rest_framework import serializers
from .models import User
from utils.password_hashing import hash_password, verify_password
from django.db.utils import IntegrityError
from rest_framework.exceptions import AuthenticationFailed
from common.exceptions import UserAlreadyExists


class RegisterSerializer(ModelSerializer):
    username = serializers.CharField(
        required=True,
        help_text="Unique username, max 12 characters"
    )
    email = serializers.EmailField(
        required=True,
        help_text="Unique email, max 20 characters"
        )
    password = serializers.CharField(
        write_only=True,
        min_length=6,
        help_text="Password (min 6 characters) max 12 character"
        )

    class Meta:
        model = User
        fields = ['id','username','email','password','is_active','created_at']

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise ValidationError("Username Already Taken")
        return value
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError("Email Already Registered")
        return value
        
    # i add try: except: for race condition errors
    def create(self, validated_data): 
        validated_data['password'] = hash_password(validated_data['password'])
        try:
            return User.objects.create(**validated_data)
        except IntegrityError:
            raise UserAlreadyExists()
        
class LoginSerializer(ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email','password']


    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = User.objects.filter(email=email).first()
        if not user:
            raise AuthenticationFailed("Invalid email or password")

        if not verify_password(password, user.password):
            raise AuthenticationFailed("Invalid email or password")

        if not user.is_active:
            raise AuthenticationFailed("Account is disabled")

        data['user'] = user
        return data
    

class LoginResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    access_token = serializers.CharField()

class RegisterSerializerResponse(serializers.Serializer):
    data = serializers.CharField()
    message = serializers.CharField()

class UserUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username']     

         




        
        