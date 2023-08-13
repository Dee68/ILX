from rest_framework import views, viewsets, status
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


class ProductApiView(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def list(self, request):
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
