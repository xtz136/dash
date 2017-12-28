
from django.contrib.auth import get_user_model
from rest_framework import serializers

from core.models import Apply
from .user import UserSerializer


class ApplySerializer(serializers.ModelSerializer):
    user = UserSerializer(
        required=False, default=serializers.CurrentUserDefault())

    class Meta:
        model = Apply
        fields = '__all__'
