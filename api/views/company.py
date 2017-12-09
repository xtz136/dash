from django_filters import rest_framework as filters
from django.contrib.auth.models import User

from rest_framework import routers, serializers, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response

from crm.models import Company
from crm import models as crm_models
from api.serializers import CompanySerializer
from api.mixins import SearchAPIViewMixin


class CompanyViewSet(SearchAPIViewMixin, viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = (filters.DjangoFilterBackend,)

    filter_fields = ('status', 'ic_status', 'license_status')
    search_fields = ('title', 'note', 'address',
                     'op_address', 'legal_people')


class FieldsInfoView(APIView):

    def get(self, request, format=None):
        model_name = request.GET.get('model', 'Company')
        data = [{'name': f.name, 'label': f.verbose_name}
                for f in getattr(crm_models, model_name)._meta.fields]
        return Response(data)
