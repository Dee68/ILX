from djoser.serializers import UserCreateSerializer
# from rest_framework.validators import UniqueValidator
# from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from account.models import Profile
# from django.contrib.auth import authenticate
# from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.utils.encoding import (
#     smart_bytes,
#     smart_str,
#     force_str,
#     DjangoUnicodeDecodeError
#     )
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from rest_framework_simplejwt.exceptions import TokenError
# from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ['id', 'email', 'username', 'password']

# class RegisterSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(max_length=20, min_length=2)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password', 'password1']
#         extra_kwargs = {
#             'password': {
#                 'write_only': True,
#                 'max_length': 20,
#                 'min_length': 2
#                 },
#             'password1': {'write_only': True}
#         }
 
#     def validate(self, attrs):
#         if attrs['password'] != attrs['password1']:
#             raise serializers.ValidationError(
#                 {'error': 'Passwords do not match'}
#                 )
#         if not attrs['username'].isalnum():
#             raise serializers.ValidationError(
#                 {'error': 'Username should only be alpha numeric characters.'}
#                 )
#         if User.objects.filter(username=attrs['username']).exists():
#             raise serializers.ValidationError(
#                 {'error': 'Use with this username already exists.'}
#                 )
#         return attrs

#     def create(self, validated_data):
#         user = User(
#             username=validated_data['username'],
#             email=validated_data['email']
#             )
#         return user


# class EmailVericationSerializer(serializers.ModelSerializer):
#     token = serializers.CharField(max_length=255)

#     class Meta:
#         model = User
#         fields = ['token']


# class LoginSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(required=True, max_length=60)
#     password = serializers.CharField(
#         max_length=20,
#         min_length=6,
#         write_only=True
#         )
#     tokens = serializers.SerializerMethodField()

#     def get_tokens(self, obj):
#         user = User.objects.get(email=obj['email'])
#         return {
#             'refresh': user.tokens()['refresh'],
#             'access': user.tokens()['access']
#         }

#     class Meta:
#         model = User
#         fields = ['email', 'password', 'tokens']

#     def validate(self, attrs):
#         email = attrs.get('email', '')
#         password = attrs.get('password', '')
#         user = authenticate(email=email, password=password)
#         if user is None:
#             raise AuthenticationFailed('Invalid credentials.')
#         if not user.is_active:
#             raise AuthenticationFailed('Account disabled, contact admin')
#         if not user.is_verified:
#             raise AuthenticationFailed(
#                 'Email not verified, verify email and try again.'
#                 )
#         return {
#             'email': user.email,
#             'username': user.username,
#             'tokens': user.tokens
#             }


# class LogoutSerializer(serializers.ModelSerializer):
#     refresh = serializers.CharField()

#     class Meta:
#         model = User
#         fields = ['refresh']

#     def validate(self, attrs):
#         self.token = attrs['refresh']
#         return attrs

#     def save(self, **kwargs):
#         try:
#             RefreshToken(self.token).blacklist()
#         except TokenError:
#             self.fail({'error': 'bad token'})


# class PasswordResetSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(required=True)

#     class Meta:
#         model = User
#         fields = ['email']


# class SetNewPasswordSerializer(serializers.Serializer):
#     password = serializers.CharField(
#         write_only=True,
#         min_length=6,
#         required=True)
#     token = serializers.CharField(write_only=True, required=True)
#     uidb64 = serializers.CharField(write_only=True, required=True)

#     class Meta:
#         fields = ['password', 'token', 'uidb64']

#     def validate(self, attrs):
#         try:
#             password = attrs.get('password')
#             token = attrs.get('token')
#             uidb64 = attrs.get('uidb64')
#             id = force_str(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(id=id)
#             if not PasswordResetTokenGenerator().check_token(user, token):
#                 raise AuthenticationFailed('The reset link is invalid', 401)
#             user.set_password(password)
#             user.save()
#         except Exception as e:
#             raise AuthenticationFailed('The reset link is invalid', 401)
#         return super().validate(attrs)
