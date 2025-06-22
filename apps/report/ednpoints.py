from rest_framework.routers import DefaultRouter
from .api import ReportViewSet

router = DefaultRouter()
router.register(r'reports', ReportViewSet, basename='report')

urlpatterns = router.urls
