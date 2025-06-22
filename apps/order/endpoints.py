from django.urls import path,include

from rest_framework.routers import DefaultRouter

from .api import OrderViewSet

routers = DefaultRouter()


routers.register('orders',OrderViewSet)


urlpatterns = [
    path('',include(routers.urls))
]