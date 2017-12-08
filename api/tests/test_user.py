import json
import pytest
from django.test import TestCase
from mixer.backend.django import mixer
from rest_framework.test import force_authenticate, APITestCase
from rest_framework.test import APIRequestFactory
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework_jwt.serializers import jwt_payload_handler,  jwt_encode_handler
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from django.test.client import encode_multipart, RequestFactory
from api import views

pytestmark = pytest.mark.django_db
User = get_user_model()


class UserTestCase(TestCase):
    def test_create(self):
        client = APIClient()
        pwd = 'abcd'
        payload = {'username': 'myname', 'password': pwd}
        resp = client.post('/api/users/', payload, format='json')
        resp.render()
        data = json.loads(resp.content)
        assert resp.status_code == 201, resp.content
        assert data['username'] == payload['username'], data
        u = User.objects.get(username=payload['username'])
        assert u.check_password(pwd)

    def test_update(self):
        pass


class LoginTestCase(TestCase):

    def test_login(self):
        user = mixer.blend('auth.User')
        pwd = 'abcd'
        user.set_password(pwd)
        user.save()

        client = APIClient()
        payload = {'username': user.username, 'password': pwd}
        resp = client.post('/api/login/account/', payload, format='json')
        resp.render()
        data = json.loads(resp.content)
        assert resp.status_code == 200, resp.content
        assert data['token'], data

        # profile
        client.credentials()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + data['token'])
        resp = client.get('/api/profile/')
        assert resp.status_code == 200
        data = json.loads(resp.content)
        assert resp.status_code == 200, resp.content
        assert data['username'] == payload['username']
        assert data['id']
