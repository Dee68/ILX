from django.urls import path
from product.views import (
    CategoryApiView,
    CategorySingleApiView,
    ProductApiView,
    ProductImageApiView
    )


urlpatterns = [
    path(
        'categories/',
        CategoryApiView.as_view(),
        name='categories'
        ),
    path(
        'category/<slug>/',
        CategorySingleApiView.as_view(),
        name='category'
        ),
    path(
        'products/',
        ProductApiView.as_view({'get': 'list'}),
        name='products'
        ),
    path(
        'products/<pk>/',
        ProductApiView.as_view({'get': 'retrieve'}),
        name='product-detail'
        ),
    path(
        'product-images/',
        ProductImageApiView.as_view(),
        name='product-images'
        )
]
