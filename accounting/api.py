from datetime import date, datetime
from django_filters import rest_framework as filters
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.filters import BaseFilterBackend

from .serializers import ReportSerializer
from .models import Report


class IsOwnerFilterBackend(BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(company=request.user.profile.company)


class DateFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        date = request.GET.get('date', None)
        if date:
            try:
                date = datetime.strptime(date, '%Y-%m-%d')
            except Exception:
                date = None
        if date is not None:
            queryset = queryset.filter(
                date__year=date.year,
                date__month=date.month)
        return queryset


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    filter_backends = (IsOwnerFilterBackend, DateFilterBackend)
