from rest_framework import viewsets

from core.models import Tag
from api.serializers import TagSerializer
from api.mixins import SearchAPIViewMixin


class TagViewSet(SearchAPIViewMixin, viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    search_fields = ('name',)
