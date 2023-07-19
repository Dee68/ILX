from .serializers import RegisterSerializer
from account.models import User, Profile
from rest_framework.response import Response
from rest_framework import generics, status


class RegisterApiView(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        user_data = serializer.data
        return Response(
            user_data,
            status=status.HTTP_201_CREATED,
            headers=headers
            )
