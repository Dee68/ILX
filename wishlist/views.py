from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from wishlist import models
from .serializers import WishListSerializer
from .models import WishList


class WishListApiView(generics.ListCreateAPIView):
    #permission_classes = (IsAuthenticated,)
    model = WishList
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer


class UserWishListItems(generics.ListAPIView):
    queryset = models.WishList.objects.all()
    serializer_class = WishListSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        user_id = self.kwargs['pk']
        qs = qs.filter(user__id=user_id)
        return qs
