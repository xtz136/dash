from rest_framework import serializers

from .models import Report
from core.serializers import AttachmentSerializer
from api.serializers import CompanySerializer


class ReportSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    data = serializers.SerializerMethodField()
    attachments = AttachmentSerializer(many=True)

    def get_data(self, obj):
        return obj.data

    class Meta:
        fields = '__all__'
        model = Report
