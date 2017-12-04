
import pytest
from mixer.backend.django import mixer
from rest_framework.test import force_authenticate, APITestCase
from rest_framework.test import APIRequestFactory

from rest_framework.test import APIClient
from rest_framework_jwt.serializers import jwt_payload_handler,  jwt_encode_handler
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from django.test.client import encode_multipart, RequestFactory
from api import views

pytestmark = pytest.mark.django_db


class TestClient(APITestCase):
    def test_access_profile(self):
        factory = APIRequestFactory()
        # Make an authenticated request to the view...
        response = self.client.get(reverse('api:user-profile'))
        assert response.status_code == 401, "没有权限访问"

    def test_auth_user_access(self):
        user = mixer.blend('auth.User')
        token = jwt_encode_handler(jwt_payload_handler(user))

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        # force_authenticate(request, token=token)
        response = self.client.get(reverse('api:user-profile'))
        assert response.status_code == 200, "有权限访问"
        assert response.data['username'] == user.username
