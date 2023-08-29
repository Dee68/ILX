from rest_framework import serializers
from .models import WishList
from product.serializers import ProductSerializer
from account.api.serializers import UserSerializer


class WishListSerializer(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField()
    product_info = serializers.SerializerMethodField()

    def get_user_info(self, obj):
        return UserSerializer(obj.user).data

    def get_product_info(self, obj):
        return ProductSerializer(obj.product).data

    class Meta:
        model = WishList
        fields = '__all__'
