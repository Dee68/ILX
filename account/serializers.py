from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from account.models import Profile
from django.contrib.auth import authenticate
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=20, min_length=2)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password1']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'max_length': 20,
                'min_length': 2
                },
            'password1': {'write_only': True}
        }
 
    def validate(self, attrs):
        if attrs['password'] != attrs['password1']:
            raise serializers.ValidationError(
                {'error': 'Passwords do not match'}
                )
        if not attrs['username'].isalnum():
            raise serializers.ValidationError(
                {'error': 'Username should only be alpha numeric characters.'}
                )
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError(
                {'error': 'Use with this username already exists.'}
                )
        return attrs

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
            )
        return user


class EmailVericationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, max_length=60)
    password = serializers.CharField(
        max_length=20,
        min_length=6,
        write_only=True
        )
    username = serializers.CharField(
        max_length=20,
        min_length=2,
        read_only=True
        )
    # tokens = serializers.CharField(max_length=70, read_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])
        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user = authenticate(email=email, password=password)
        # user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('User not found.')
        # if not user.check_password(password):
        #     raise AuthenticationFailed('Incorrect credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed(
                'Email not verified, verify email and try again.'
                )
        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }
