from django_filters import rest_framework as filters

from .serializers import Report

class ReportFilterSet(filters.FilterSet):
    start = filters.DateFilter(field_name="start_date")
    end = filters.DateFilter(field_name="end_date")

    class Meta:
        model = Report
        fields = ['start','end']
