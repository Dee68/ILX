from rest_framework import (
    views,
    status,
    generics)
from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .serializers import (
    CategorySerializer,
    ProductSerializer
    )
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


class ProductApiView(generics.ListAPIView):
    model = Product
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductCreateView(generics.CreateAPIView):
    model = Product
    serializer_class = ProductSerializer


class ProductDetailView(generics.RetrieveAPIView):
    model = Product
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDeleteView(generics.DestroyAPIView):
    model = Product
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
