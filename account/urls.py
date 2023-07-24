from django.urls import path
from account.views import (
    RegisterApiView,
    VerifyEmail,
    LoginApiView,
    LogoutApiView,
    PasswordResetApiView,
    PasswordTokenCheckApiView,
    SetNewPasswordApiView
    )
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterApiView.as_view(), name='register'),
    path('verify-email/', VerifyEmail.as_view(), name='verify-email'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', LoginApiView.as_view(), name='login'),
    path('logout/', LogoutApiView.as_view(), name='logout'),
    path(
        'request-password-reset/',
        PasswordResetApiView.as_view(),
        name='reset-password'
        ),
    path(
        'password-reset/<uidb64>/<token>/',
        PasswordTokenCheckApiView.as_view(),
        name='password-reset-confirm'
        ),
    path(
        'password-reset-complete/',
        SetNewPasswordApiView.as_view(),
        name='password-reset-complete'
        )
]
