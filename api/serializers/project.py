from django.contrib.auth import get_user_model
from rest_framework import serializers

from project.models import Member, Group, Category, Project
from .user import UserSerializer
from .tag import TagSerializer
from .company import CompanySerializer

User = get_user_model()


class MemberSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Member
        fields = ('id', 'project', 'user', 'role')


class GroupSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True)

    class Meta:
        model = Group
        fields = ('id', 'project', 'members')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title')


class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(
        required=False, default=serializers.CurrentUserDefault())
    category = CategorySerializer(required=False)
    deleted_by = UserSerializer(required=False)
    completed_by = UserSerializer(required=False)
    tags = serializers.SerializerMethodField()
    members = serializers.SerializerMethodField()
    company = CompanySerializer(required=False)

    def get_members(self, obj):
        return [MemberSerializer(t).data for t in obj.members.all()]

    def get_tags(self, obj):
        return [TagSerializer(t).data for t in obj.tags.all()]

    class Meta:
        model = Project
        fields = '__all__'

    def validate_title(self, value):
        if Project.objects.filter(title=value).exists():
            raise serializers.ValidationError('已存在相同名称的项目')
        return value
