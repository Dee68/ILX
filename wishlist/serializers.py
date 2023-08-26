from rest_framework import serializers
from .models import WishList
from product.serializers import ProductSerializer


class WishListSerializer(serializers.ModelSerializer):
    # user_info = serializers.SerializerMethodField()
    # product_info = serializers.SerializerMethodField()

    # def get_user_info(self, obj):
    #     return obj.user

    # def get_product_info(self, obj):
    #     return obj.product

    class Meta:
        model = WishList
        fields = '__all__'
