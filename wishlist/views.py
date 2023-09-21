from rest_framework import generics, status
from rest_framework.response import Response
from wishlist import models
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .serializers import WishListSerializer
from .models import WishList


class WishListApiView(generics.ListCreateAPIView):
    model = WishList
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer


class UserWishListItems(generics.ListAPIView):
    model = WishList
    queryset = models.WishList.objects.all()
    serializer_class = WishListSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        user_id = self.kwargs['pk']
        qs = qs.filter(user__id=user_id)
        return qs


@api_view(('POST',))
@csrf_exempt
def remove_from_list(request):
    if request.method == 'POST':
        wishlist_id = request.POST.get('wishlist_id')
        res = models.WishList.objects.filter(id=wishlist_id).delete()
        msg = {'bool': False}
        if res:
            msg = {'bool': True}
    return Response(msg, status=status.HTTP_202_ACCEPTED)
