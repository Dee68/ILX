from django.urls import path
from product.views import (
    CategoryApiView,
    CategorySingleApiView,
    ProductApiView
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
    path('products/', ProductApiView.as_view(), name='products')
]
