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

    seller = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Product
        fields = (
            'name',
            'status',
            'price',
            'category',
            'description',
            'seller',
            'quantity',
            'photo1',
            'photo2',
            'photo3',
            'photo4',
            'photo5',
            )

    def create(self, validated_data):
        user = self.context['request'].user
        product = Product.objects.create(
            name=validated_data['name'],
            status=validated_data['status'],
            price=validated_data['price'],
            category=validated_data['category'],
            quantity=validated_data['quantity'],
            seller=user,
            photo1=validated_data['photo1'],
            photo2=validated_data['photo2'],
            photo3=validated_data['photo3'],
            photo4=validated_data['photo4'],
            photo5=validated_data['photo5'],
        )
        
        return product
