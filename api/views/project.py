from rest_framework import routers, serializers, viewsets
from django_filters import rest_framework as filters
from django.contrib.auth.models import User

from core.models import Tag
from crm.views.mixins import SearchViewMixin
from project import models


class TagSerializer(serializers.Serializer):
    pass


class MembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'id')


class ProjectSerializer(serializers.ModelSerializer):
    members = MembersSerializer(many=True)
    owner = MembersSerializer(read_only=True)
    tags = serializers.SerializerMethodField()
    client = serializers.StringRelatedField()

    class Meta:
        model = models.Project
        fields = ('id', 'title', 'description', 'logo', 'members', 'tags',
                  'created', 'updated', 'owner', 'client', 'category')

    def get_tags(self, obj):
        return [t.to_json() for t in obj.tags.all()]

    def create(self, validated_data):
        members = self.context['request'].POST.getlist('members')
        tags = self.context['request'].POST.getlist('tags')
        validated_data.pop('members')
        # FIXME buggy
        validated_data['owner'] = User.objects.get(
            id=self.context['request'].POST.getlist('owner')[0])

        project = super(ProjectSerializer, self).create(validated_data)
        for m in User.objects.filter(id__in=members):
            project.members.add(m)
        for t in Tag.objects.filter(id__in=tags):
            project.tags.add(t)
        return project


class ProjectViewSet(SearchViewMixin, viewsets.ModelViewSet):
    queryset = models.Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('title', )
    search_fields = ('title', 'description')

    def get_queryset(self):
        queryset = super(ProjectViewSet, self).get_queryset()
        q = self.request.GET.get('q', '').strip()
        if q:
            queryset = self.get_search_results(queryset, q)
        return queryset
