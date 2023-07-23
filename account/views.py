from .serializers import (
    UserSerializer,
    RegisterSerializer,
    EmailVericationSerializer,
    LoginSerializer
    )
from django.urls import reverse
from django.conf import settings
from account.models import User, Profile
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
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
            username=request.data.get('username'),
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
        abs_link = 'http://'+current_site+rel_link+'?token='+str(token.access_token)
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
    # permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        # email = request.data['email']
        # password = request.data['password']
        # user = User.objects.filter(email=email).first()
        # if user is None:
        #     raise AuthenticationFailed('User not found.')
        # if not user.check_password(password):
        #     print(user.email)
        #     raise AuthenticationFailed('Incorrect credentials, try again')
        # if not user.is_active:
        #     raise AuthenticationFailed('Account disabled, contact admin')
        # if not user.is_verified:
        #     raise AuthenticationFailed(
        #         'Email not verified, verify email and try again.'
        #         )
        # return Response({'message': 'success'})
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
