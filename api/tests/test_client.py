import pytest
from mixer.backend.django import mixer
from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory

from django.test.client import encode_multipart, RequestFactory
from api import views

pytestmark = pytest.mark.django_db


class TestClient:
    def test_access(self):
        factory = APIRequestFactory()
        user = mixer.blend('auth.User', is_superuser=True)
        # Make an authenticated request to the view...
        request = factory.get('/api/fields_info/')

        response = views.FieldsInfoView.as_view()(request)
        assert response.status_code == 401, "没有权限访问"

        force_authenticate(request, user=user)
        response = views.FieldsInfoView.as_view()(request)
        assert response.status_code == 200, "有权限访问"
