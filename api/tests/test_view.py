import pytest
import json
from unittest.mock import patch
from django.urls import reverse
from django.test import TestCase
from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework.test import APIRequestFactory, force_authenticate, APIClient
from mixer.backend.django import mixer

from core.models import AccessToken, Profile, Tag
from api import views
from api.views import issue_token

pytestmark = pytest.mark.django_db
User = get_user_model()


class TagTestCase(TestCase):
    def setUp(self):
        super(TagTestCase, self).setUp()
        self.tags = mixer.cycle(10).blend('core.Tag')

    def test_list(self):
        n = 10
        tags = self.tags
        factory = APIRequestFactory()
        request = factory.get('/api/tags/')
        view = views.TagViewSet.as_view(
            {'get': 'list', 'post': 'create'})
        response = view(request)
        assert response.status_code == 401

        # test with token
        user = mixer.blend('auth.User')
        token = issue_token(user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token['token'])

        response = client.get('/api/tags/')
        response.render()
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data['count'] == n
        assert len(data['results']) >= 1

    def test_search(self):
        # test with token
        user = mixer.blend('auth.User')
        token = issue_token(user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token['token'])

        response = client.get('/api/tags/search/?q=')
        response.render()
        assert response.status_code == 200
        data = json.loads(response.content)
        assert isinstance(data, list)
        assert len(data) <= 10

        response = client.get('/api/tags/search/?q=' + self.tags[0].name)
        response.render()
        assert response.status_code == 200
        data = json.loads(response.content)
        assert isinstance(data, list)
        assert len(data) == 1

    def test_create(self):

        client = APIClient()
        tag = {'name': '标签', 'colour': '#ffffff'}
        response = client.post('/api/tags/', tag)
        assert response.status_code == 401

        user = mixer.blend('auth.User')
        token = issue_token(user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token['token'])
        response = client.post('/api/tags/', tag)
        response.render()
        assert response.status_code == 201
        data = json.loads(response.content)
        assert data['name'] == tag['name']
        assert data['colour'] == tag['colour']
        assert Tag.objects.get(pk=data['id'])


class UserTestCase(TestCase):
    pass
