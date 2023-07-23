from django.urls import path
from account.views import RegisterApiView, VerifyEmail, LoginApiView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView
    )

urlpatterns = [
    path('register/', RegisterApiView.as_view(), name='register'),
    path('verify-email/', VerifyEmail.as_view(), name='verify-email'),
    # path('jwt/token/', TokenObtainPairView.as_view(), name='create-token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', LoginApiView.as_view(), name='login')
]
