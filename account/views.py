from .serializers import (
    RegisterSerializer,
    EmailVericationSerializer,
    LoginSerializer,
    LogoutSerializer,
    PasswordResetSerializer,
    SetNewPasswordSerializer
    )
from django.urls import reverse
from django.conf import settings
from account.models import User, Profile
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import (
    smart_bytes,
    smart_str,
    force_str,
    DjangoUnicodeDecodeError
    )
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics, status, views
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from account.utils import Util
import jwt


class RegisterApiView(generics.CreateAPIView):

    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user = User.objects.create_user(
            username=serializer.data.get('username'),
            email=serializer.data.get('email')
            )
        user.set_password(request.data.get('password'))
        user.save()
        user_data = serializer.data
        token = RefreshToken.for_user(user)
        user_data["tokens"] = {
            "refresh": str(token),
            "access": str(token.access_token)
            }
        headers = self.get_success_headers(serializer.data)
        email_subject = 'Account verification'
        msg = 'please use the link below to verify your account'
        current_site = get_current_site(request).domain
        rel_link = reverse('verify-email')
        abs_link = 'http://'+current_site+rel_link+'?token='\
            + str(token.access_token)
        email_body = f'Hi {user.username}, {msg} {abs_link}'
        data = {
            'user': user.email,
            'email_subject': email_subject,
            'email_body': email_body
        }

        Util.send_mail(data)

        return Response(
            {'message': 'Verify your email to activate account',
                'user': user_data['username'],
                'user-tokens': user_data['tokens']},
            status=status.HTTP_201_CREATED,
            headers=headers
            )


class VerifyEmail(views.APIView):
    serializer_class = EmailVericationSerializer
    token_param_config = openapi.Parameter('token',
                                           in_=openapi.IN_QUERY,
                                           description='Description',
                                           type=openapi.TYPE_STRING
                                           )

    @swagger_auto_schema(manual_parameters=[token_param_config])                              
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=['HS256']
                )
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response(
                {'message': 'Account verified successfully'},
                status=status.HTTP_200_OK
                )
        except jwt.ExpiredSignatureError:
            return Response(
                {'error': 'Verification token has expired'},
                status=status.HTTP_400_BAD_REQUEST
                )
        except jwt.exceptions.DecodeError:
            return Response(
                {'error': 'Invalid token'},
                status=status.HTTP_400_BAD_REQUEST
                )


class LoginApiView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutApiView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PasswordResetApiView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            email_subject = 'Password Reset'
            msg = 'please use the link below to reset your password'
            current_site = get_current_site(request).domain
            rel_link = reverse(
                'password-reset-confirm',
                kwargs={'uidb64': uidb64, 'token': token}
                )
            abs_link = 'http://'+current_site+rel_link
            email_body = f'Hi {user.username}, {msg} {abs_link}'
            data = {
                'user': user.email,
                'email_subject': email_subject,
                'email_body': email_body
                }
            Util.send_mail(data)
            return Response(
                {'message': 'A link has been sent to your email'},
                status=status.HTTP_200_OK
                )
        else:
            return Response(
                {'error': 'Email not in database'},
                status=status.HTTP_400_BAD_REQUEST
                )


class PasswordTokenCheckApiView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token not valid'})
            return Response(
                {
                    'success': True,
                    'message': 'Credentials valid',
                    'uidb64': uidb64,
                    'token': token
                },
                status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError:
            if not PasswordResetTokenGenerator().check_token(user):
                return Response({'error': 'Invalid token'})


class SetNewPasswordApiView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {'message': 'passwor reset success'},
            status=status.HTTP_200_OK
            )
