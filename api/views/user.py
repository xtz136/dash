from crm.models import Company
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import routers, serializers, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import list_route
from rest_framework.permissions import IsAuthenticated
from ..permissions import IsPostOrIsAuthenticated

from crm import models as crm_models


class UserSerializer(serializers.HyperlinkedModelSerializer):
    avatar = serializers.CharField(
        max_length=200,
        default='https://avatars3.githubusercontent.com/u/2841480?s=400&u=ad4b4f84cad78433b1635b26f21b49b3bb4fa5dc&v=4')
    notifyCount = serializers.IntegerField(default=12)

    def create(self, validated_data):
        user = User(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        user.profile.mobile = validated_data.get('mobile', '')
        user.profile.avatar = validated_data.get('avatar', '')
        user.profile.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'email', 'is_staff', 'id',
                  'avatar', 'notifyCount', 'password')
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('notifyCount', )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsPostOrIsAuthenticated]

    @list_route(methods=['get'], url_name='profile')
    def profile(self, request):
        instance = request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
