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


# class ImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductImage
#         fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    # queryset = ProductImage.objects.all()
    # product_images = serializers.PrimaryKeyRelatedField(
    #     many=True,
    #     queryset=queryset
    # )
 
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'status',
            'price',
            'category',
            'seller',
            'created_at',
            'photo1',
            'photo2',
            'photo3',
            'photo4',
            'photo5',
            'photo6',
            )
