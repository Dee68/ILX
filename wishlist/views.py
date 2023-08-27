from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import WishListSerializer
from .models import WishList


class WishListApiView(generics.ListAPIView):
    #permission_classes = (IsAuthenticated,)
    model = WishList
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer


class WishListCreateView(generics.CreateAPIView):
    #permission_classes = (IsAuthenticated,)
    model = WishList
    serializer_class = WishListSerializer
