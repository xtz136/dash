from django_filters import rest_framework as filters
from django.contrib.auth.models import User

from rest_framework import routers, serializers, viewsets, status
from rest_framework.response import Response

from crm.models import Company
from api.serializers import CompanySerializer
from api.mixins import SearchAPIViewMixin


class CompanyViewSet(SearchAPIViewMixin, viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('title', 'ic_status', 'status')
    search_fields = ('title', 'address', 'op_address')
