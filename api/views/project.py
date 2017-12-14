from mimetypes import guess_type
from django_filters import rest_framework as filters
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.parsers import JSONParser, FileUploadParser, FormParser, MultiPartParser
from rest_framework import routers, serializers, viewsets, status, views
from rest_framework.response import Response
from rest_framework.decorators import detail_route

from project.models import Project, Category, Member, File, Folder
from project.factory import FileFactory
from crm.models import Company
from core.models import Tag
from api.serializers import ProjectSerializer, FileSerializer
from api.filters import SearchFilter


User = get_user_model()


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = (SearchFilter, filters.DjangoFilterBackend,)
    filter_fields = ('owner', )
    search_fields = ('title', 'description')
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_relation(self, request, pk_field, model, model_field='pk'):
        pk = request.data.pop(pk_field, None)
        obj = None
        if pk is not None:
            lookup = {model_field: pk}
            try:
                obj = model.objects.get(**lookup)
            except model.DoesNotExist:
                pass
        return obj

    def get_relations(self, request, pk_field, model):
        pks = request.data.pop(pk_field, None)
        objs = model.objects.none()
        if pks is not None:
            objs = model.objects.filter(pk__in=pks)
        return objs

    def create(self, request):
        company = self.get_relation(
            request, 'company', Company, model_field='title')
        category = self.get_relation(request, 'category', Category)
        users = self.get_relations(request, 'members', User)
        tags = self.get_relations(request, 'tags', Tag)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        obj.company = company
        obj.category = category
        obj.add_members(users)
        obj.add_tags(tags)
        obj.active()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)

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
        return Response({'ok': 'ok'}, status=201)


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
