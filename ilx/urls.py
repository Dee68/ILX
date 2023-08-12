"""ilx URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
#from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from account.api.views import (
    ProfileDetailView,
    ProfileListView,
    ProfileUpdateView,
    )


schema_view = get_schema_view(
   openapi.Info(
      title="ILX API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.ilxapp.com/policies/terms/",
      contact=openapi.Contact(email="mrdee316@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        '',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
        ),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('djoser.urls.authtoken')),
    #path('auth/', include('djoser.social.urls')),
    path('api/', include('product.urls')),
    path('api/profiles', ProfileListView.as_view(), name='profiles'),
    path(
        'api/profiles/<int:user>/',
        ProfileDetailView.as_view(),
        name='profile'
        ),
    path(
        'api/profiles/<int:user>/update/',
        ProfileUpdateView.as_view(),
        name='profile-update'
        ),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]
