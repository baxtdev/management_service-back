from django.urls import path,include

from rest_framework.routers import DefaultRouter

from .api import ClientViewSet

routers = DefaultRouter()

routers.register('customers',ClientViewSet)


urlpatterns = [
     path('',include(routers.urls))
]