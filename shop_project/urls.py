"""shop_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from product import views
from users import views as user_views
from .constants import LIST_CREATE_DICT
from . import swagger

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/test/', views.test_api),
    path('api/v1/products/', views.ProductListCreateAPIView.as_view()),
    path('api/v1/products/<int:id>/', views.product_detail_api_view),
    path('api/v1/users/registration/', user_views.registration_view),
    path('api/v1/users/authorization/', user_views.authorization_view),
    path('api/v1/categories/', views.CategoryListAPIView.as_view()),
    path('api/v1/categories/<int:pk>/', views.CategoryDetailAPIView.as_view()),
    path('api/v1/tags/', views.TagModelViewSet.as_view(LIST_CREATE_DICT)),
    path('api/v1/tags/<int:pk>/', views.TagModelViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update',
                                                                 'put': 'update', 'delete': 'destroy'})),
]

urlpatterns += swagger.urlpatterns
