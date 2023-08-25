from django.urls import path
from product.views import (
    CategoryApiView,
    CategorySingleApiView,
    ProductApiView,
    ProductCreateView,
    ProductDetailView,
    ProductDeleteView,
    ProductUpdateView,
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
        ProductApiView.as_view(),
        name='products'
        ),
    path(
        'products/create/',
        ProductCreateView.as_view(),
        name='product-create'
        ),
    path(
        'products/<int:pk>/',
        ProductDetailView.as_view(),
        name='product-detail'
    ),
    path(
        'products/<int:pk>/delete/',
        ProductDeleteView.as_view(),
        name='product-delete'
    ),
    path(
        'products/<int:pk>/update/',
        ProductUpdateView.as_view(),
        name='product-update'
    ),
]
