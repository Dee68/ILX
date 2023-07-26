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
    model = Product
    fields = '__all__'
