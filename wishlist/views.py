from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import WishListSerializer
from .models import WishList


class WishListApiView(generics.ListCreateAPIView):
    #permission_classes = (IsAuthenticated,)
    model = WishList
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer
