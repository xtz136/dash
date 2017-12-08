from django_filters import rest_framework as filters
from django.contrib.auth.models import User

from rest_framework import routers, serializers, viewsets, status
from rest_framework.response import Response

from project.models import Project
from api.serializers import ProjectSerializer
from api.mixins import SearchAPIViewMixin


class ProjectViewSet(SearchAPIViewMixin, viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('title', 'owner')
    search_fields = ('title', 'description')

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
