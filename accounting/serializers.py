from rest_framework import serializers

from .models import Result
from core.serializers import AttachmentSerializer
from api.serializers import CompanySerializer


class ResultSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    data = serializers.SerializerMethodField()
    attachments = AttachmentSerializer(many=True)

    def get_data(self, obj):
        return obj.data

    class Meta:
        fields = '__all__'
        model = Result
