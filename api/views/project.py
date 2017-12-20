from mimetypes import guess_type
import logging
from django_filters import rest_framework as filters
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.parsers import JSONParser, FileUploadParser, FormParser, MultiPartParser
from rest_framework import routers, serializers, viewsets, status, views
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from notifications.signals import notify
from rest_framework_extensions.mixins import NestedViewSetMixin


from project.models import Project, Category, Member, File, Folder
from project.factory import FileFactory
from crm.models import Company
from core.models import Tag, Follower
from api.serializers import ProjectSerializer, FileSerializer
from api.filters import SearchFilter


User = get_user_model()

logger = logging.getLogger(__file__)


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
        pks = request.data.pop(pk_field, [])
        objs = model.objects.none()
        pks = [pk for pk in pks if isinstance(pk, int) or pk.isdigit()]
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
                  url_path='add-files')
    def add_files(self, request, pk=None):
        logger.debug('project add files')
        project = self.get_object()
        files = request.data.get('files', [])
        folder = request.data.get('folder', None)
        if folder:
            try:
                folder = Folder.objects.get(id=folder)
            except Folder.DoesNotExist:
                folder = None
        description = request.data.get('description', '')
        followers = request.data.get('followers', [])
        files = File.objects.filter(id__in=files)
        files.update(project=project, folder=folder,
                     description=description)

        for f in files:
            for user in User.objects.filter(id__in=followers):
                logger.debug('user {0} follow file {1}'.format(user, f))
                if not f.followers.filter(user=user).exists():
                    f.followers.create(user=user)
                # Follower.objects.get_or_create(user=user, content_object=f)
                # send notifications
                notify.send(request.user, recipient=user,
                            verb='创建文件',
                            action_object=f,
                            description='用户{user}上传了文件{file}'.format(
                                user=request.user, file=f),
                            level='info')

        s = FileSerializer(files, many=True)
        return Response(s.data)


class FileUploadView(views.APIView):
    parser_classes = (MultiPartParser,)

    def to_result(self, f):

        return {"name": f.name,
                "id": f.id,
                "type": guess_type(f.file.path)[0],
                "size": f.file.size,
                "url": f.file.url,
                "thumbnailUrl": f.file.url,
                "deleteUrl": reverse('api:upload', kwargs={'filename': f.pk}),
                "deleteType": "DELETE"}

    def put(self, request, filename, format=None):
        file_obj = request.data['file']
        f = FileFactory.create(file=file_obj, creator=request.user)
        data = {'files': [self.to_result(f)]}
        return Response(data, status=201)
