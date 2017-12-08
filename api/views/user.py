from crm.models import Company
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import routers, serializers, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import list_route
from ..permissions import IsPostOrIsAuthenticated, IsAdminOrIsSelf

from api.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsPostOrIsAuthenticated, IsAdminOrIsSelf]


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def profile_view(request, format=None):
    return Response(UserSerializer(request.user).data)
