from rest_framework.generics import get_object_or_404
from rest_framework import viewsets, serializers, status
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin
from mptt.templatetags.mptt_tags import cache_tree_children

from project.models import Folder, Project
from api.serializers import FolderSerializer


def recursive_node_to_dict(node):
    result = {
        'label': node.name,
        'value': str(node.id),
        'key': node.id
    }
    children = [recursive_node_to_dict(c) for c in node.get_children()]
    if children:
        result['children'] = children
    return result


class FolderViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer

    def get_project(self):
        lookup = self.get_parents_query_dict()
        obj = get_object_or_404(Project.objects.all(), id=lookup['project'])
        # TODO
        # self.check_object_permissions(self.request, obj)
        return obj

    def list(self, request, *args, **kwargs):
        folders = self.filter_queryset(self.get_queryset())
        root_nodes = cache_tree_children(folders)
        data = [
            recursive_node_to_dict(node) for node in root_nodes
        ]
        return Response(data)

    def get_serializer(self, *args, **kwargs):
        if 'data' in kwargs:
            kwargs['data'] = dict(
                kwargs['data'], **self.get_parents_query_dict())
        return super(FolderViewSet, self).get_serializer(*args, **kwargs)
