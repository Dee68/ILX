from rest_framework import serializers
from product.models import Category, Product


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CategorySerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True)

    class Meta:
        model = Category
        fields = ('id', 'title', 'description', 'image', 'children',)


class ProductSerializer(serializers.ModelSerializer):

    seller_username = serializers.SerializerMethodField()
    seller_county = serializers.SerializerMethodField()
    seller_phone_number = serializers.SerializerMethodField()
    seller_city = serializers.SerializerMethodField()

    def get_seller_username(self, obj):
        return obj.seller.username

    def get_seller_county(self, obj):
        return obj.seller.profile.county

    def get_seller_phone_number(self, obj):
        return obj.seller.profile.phone_number

    def get_seller_city(self, obj):
        return obj.seller.profile.city

    class Meta:
        model = Product
        fields = '__all__'
