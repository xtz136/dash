from mimetypes import guess_type
from django_filters import rest_framework as filters
from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.parsers import JSONParser, FileUploadParser, FormParser, MultiPartParser
from rest_framework import routers, serializers, viewsets, status, views
from rest_framework.response import Response
from rest_framework.decorators import detail_route

from project.models import Project, Category, Member, File, Folder
from project.factory import FileFactory
from core.models import Tag
from api.serializers import ProjectSerializer, FileSerializer
from api.filters import SearchFilter


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = (SearchFilter, filters.DjangoFilterBackend,)
    filter_fields = ('owner', )
    search_fields = ('title', 'description')
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def create(self, request):
        cat_id = request.data.pop('category', None)
        tags = request.data.pop('tags', None)
        members = request.data.pop('members', None)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        if cat_id:
            obj.category = Category.objects.get(pk=cat_id)
            obj.save()
        if tags:
            tags = Tag.objects.filter(id__in=tags)
            for t in tags:
                obj.tags.add(t)
        # TODO: member also has role
        if members:
            users = User.objects.filter(id__in=members)
            for user in users:
                Member.objects.get_or_create(project=obj, user=user)

        obj.active()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @detail_route()
    def files(self, request, pk=None):
        # TODO: check have permissions
        project = self.get_object()
        queryset = File.objects.filter(project=project)
        serializer = FileSerializer(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)

    @detail_route(methods=['post'],
                  url_path='add-file',
                  parser_classes=((MultiPartParser,)))
    def add_file(self, request, pk=None):
        project = self.get_object()
        return Response(s.data, status=201, headers=headers)


class FileUploadView(views.APIView):
    parser_classes = (MultiPartParser,)

    def to_result(self, f):

        return {"name": f.name,
                "type": guess_type(f.file.path)[0],
                "size": f.file.size,
                "url": f.file.url,
                "thumbnailUrl": f.file.url,
                "deleteUrl": reverse('api:upload', kwargs={'filename': f.pk}),
                "deleteType": "DELETE"}

    def put(self, request, filename, format=None):
        file_obj = request.data['file']
        f = FileFactory.create(file=file_obj)
        data = {'files': [self.to_result(f)]}
        return Response(data, status=201)
