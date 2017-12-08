from django.contrib.auth import get_user_model
from rest_framework import serializers

from crm.models import Company
from .user import UserSerializer

User = get_user_model()


class CompanySerializer(serializers.ModelSerializer):
    saleman = UserSerializer(required=False)
    bookkeeper = UserSerializer(required=False)

    class Meta:
        model = Company
        fields = '__all__'
