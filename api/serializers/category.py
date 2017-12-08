from django.contrib.auth import get_user_model
from rest_framework import serializers

from project.models import Member, Group, Category, Project
from .user import UserSerializer
from .tag import TagSerializer

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
    colour = serializers.CharField(required=False)

    class Meta:
        model = Category
        fields = ('id', 'title', 'colour')


def _validate_user(value):
    if isinstance(value, User):
        return value
    raise serializers.ValidationError("must be a user instance")


class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(required=False)
    category = CategorySerializer(required=False)
    deleted_by = UserSerializer(required=False)
    completed_by = UserSerializer(required=False)
    tags = serializers.SerializerMethodField()

    def get_tags(self, obj):
        return [TagSerializer(t).data for t in obj.tags.all()]

    class Meta:
        model = Project
        fields = '__all__'

    def validate_title(self, value):
        if Project.objects.filter(title=value).exists():
            raise serializers.ValidationError('已存在相同名称的项目')
        return value

    def validate_deleted_by(self, value):
        return _validate_user(value)

    def validate_completed_by(self, value):
        return _validate_user(value)

    # def validate_category(self, value):
    #     return _validate_user(value)
