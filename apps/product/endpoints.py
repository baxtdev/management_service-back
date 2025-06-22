from django.urls import path,include

from rest_framework.routers import DefaultRouter

from .api import ProductViewSet

routers = DefaultRouter()

routers.register('products',ProductViewSet)



urlpatterns = [
    path('',include(routers.urls))
]