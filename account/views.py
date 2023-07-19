from .serializers import RegisterSerializer, EmailvericationSerializer
from django.urls import reverse
from django.conf import settings
from account.models import User, Profile
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .utils import Util
import jwt


class RegisterApiView(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user = serializer.instance
        user_data = serializer.data
        obj = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(obj).access_token
        headers = self.get_success_headers(serializer.data)
        email_subject = 'Account verification'
        msg = 'please use the link below to verify your account'
        current_site = get_current_site(request).domain
        rel_link = reverse('verify-email')
        abs_link = 'http://'+current_site+rel_link+'?token='+str(token)
        email_body = f'Hi {user.username}, {msg} {abs_link}'
        data = {
            'user': user.email,
            'email_subject': email_subject,
            'email_body': email_body
        }

        Util.send_mail(data)

        return Response(
            user_data,
            status=status.HTTP_201_CREATED,
            headers=headers
            )


class VerifyEmail(generics.GenericAPIView):
    serializer_class = EmailvericationSerializer
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
