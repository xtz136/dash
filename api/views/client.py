from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers, viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters


from crm.views.mixins import SearchViewMixin
from crm import models as crm_models


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = crm_models.Company
        lookup_field = 'id'
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CompanySerializer, self).__init__(*args, **kwargs)
        fields = self.context['request'].query_params.getlist('fields')
        if fields:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for name in existing - allowed:
                self.fields.pop(name)


class CompanyViewSet(SearchViewMixin, viewsets.ModelViewSet):
    queryset = crm_models.Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('status', 'ic_status', 'license_status')
    search_fields = ('title', 'note', 'address',
                     'op_address', 'legal_people')

    def get_queryset(self):
        queryset = super(CompanyViewSet, self).get_queryset()
        q = self.request.GET.get('q', '').strip()
        if q:
            queryset = self.get_search_results(queryset, q)
        return queryset


class FieldsInfoView(APIView):

    def get(self, request, format=None):
        model_name = request.GET.get('model', 'Company')
        data = [{'name': f.name, 'label': f.verbose_name}
                for f in getattr(crm_models, model_name)._meta.fields]
        return Response(data)
