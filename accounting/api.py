from django_filters import rest_framework as filters
from django.contrib.auth import get_user_model
from rest_framework import viewsets

from .serializers import ResultSerializer
from .models import Result


class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('date', )
