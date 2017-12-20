from django_filters import rest_framework as filters
from rest_framework.generics import get_object_or_404
from rest_framework import viewsets, serializers, status
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin

from project.models import Folder, Project, File
from api.serializers import FileSerializer
from api.filters import SearchFilter


class FileViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    filter_backends = (SearchFilter, filters.DjangoFilterBackend,)
    filter_fields = ('folder', )
    search_fields = ('name', 'description')

    def get_serializer(self, *args, **kwargs):
        if 'data' in kwargs:
            kwargs['data'] = dict(
                kwargs['data'], **self.get_parents_query_dict())
        return super(FileViewSet, self).get_serializer(*args, **kwargs)
