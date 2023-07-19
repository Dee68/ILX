from django.urls import path
from .views import RegisterApiView, VerifyEmail

urlpatterns = [
    path('register/', RegisterApiView.as_view(), name='register'),
    path('verify-email/', VerifyEmail.as_view(), name='verify-email')
]
