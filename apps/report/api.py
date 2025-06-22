from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend

from .serializers import ReportSerializer,Report
from .services import ReportService
from .filters import ReportFilterSet

class ReportViewSet(ReportService,ReadOnlyModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend,SearchFilter]
    filterset_class = ReportFilterSet

    