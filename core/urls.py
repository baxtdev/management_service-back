"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include

from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

from apps.client.endpoints import urlpatterns as client_urls
from apps.order.endpoints import urlpatterns as order_urls
from apps.product.endpoints import urlpatterns as product_urls
from apps.report.ednpoints import urlpatterns as report_urls
from .yasg import urlpatterns as doc_url



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include(client_urls)),
    path('api/',include(order_urls)),
    path('api/',include(product_urls)),
    path('api/',include(report_urls)),
    path('',include(doc_url)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

