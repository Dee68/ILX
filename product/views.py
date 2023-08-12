from rest_framework import views, viewsets
from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ImageSerializer
    )
from product.models import Category, Product, ProductImage


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


class ProductApiView(viewsets.ModelViewSet):
    def list(self, request):
        queryset = Product.objects.all().order_by('-created_at')
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Product.objects.all().order_by('-created_at')
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


class ProductImageApiView(views.APIView):
    def get(self, requset):
        queryset = ProductImage.objects.all()
        serializer = ImageSerializer(queryset, many=True)
        return Response(serializer.data)
