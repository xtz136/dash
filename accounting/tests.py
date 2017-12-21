import pytest
from mixer.backend.django import mixer
from django.test import TestCase
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

pytestmark = pytest.mark.django_db
User = get_user_model()

from .models import *
from .serializers import *


class TestResult(TestCase):

    def test_create(self):
        company = mixer.blend('crm.Company')
        user = mixer.blend('auth.User')
        date = now().date()
        result = Result.objects.create(
            company=company, bookkeeper=user, date=date, data={})
        assert result.date == date
        assert isinstance(result.data, dict)
        assert result.bookkeeper == user
        assert result.company == company

    def test_serializer(self):
        company = mixer.blend('crm.Company')
        user = mixer.blend('auth.User')
        date = now().date()
        files = [
            SimpleUploadedFile(
                "file%s.mp4" % i, b"file_content", content_type="video/mp4") for i in range(100)]
        result = Result.objects.create(
            company=company, bookkeeper=user, date=date, data={})
        for f in files:
            a = Attachment(content_object=result, file=f)
            a.save()
        s = ResultSerializer(result)
        assert s.data
        assert s.data['id']
        assert isinstance(s.data['data'], dict), type(s.data['data'])
        assert s.data['company']['title']
        assert len(s.data['attachments']) == 100
