import django_filters
from django import forms
from django.http.request import QueryDict

from .models import Company


class CompanyFilter(django_filters.FilterSet):
    class Meta:
        model = Company
        fields = ('status', 'ic_status', 'license_status')

    def __init__(self, data, *args, **kwargs):
        if data is None or not data.get('status', None):
            data = QueryDict.fromkeys(data or {}, mutable=True)
            data['status'] = '有效'
        super(CompanyFilter, self).__init__(data, *args, **kwargs)
