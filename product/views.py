from rest_framework import views
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .serializers import CategorySerializer, ProductSerializer
from product.models import Category, Product


class CategoryApiView(views.APIView):

    def get(self, request):
        queryset = Category.objects.viewable()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)


class CategorySingleApiView(views.APIView):
    def get(self, request, slug):
        category = Category.objects.get(slug=slug)
        serializer = CategorySerializer(category, many=False)
        return Response(serializer.data)


class ProductApiView(views.APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
