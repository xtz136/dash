import pytest
import json
import unittest
from unittest.mock import patch
from django.urls import reverse
from django.test import TestCase
from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework.test import APIRequestFactory, force_authenticate, APIClient
from mixer.backend.django import mixer

from project.factory import ProjectFactory
from core.models import AccessToken, Profile, Tag
from project.models import *
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
    def test_list(self):
        pass

    def test_create(self):
        pass

    def test_retrive(self):
        pass

    def test_update(self):
        pass


class BaseTestViewSet:
    api_endpoint = None
    count = 10

    @classmethod
    def setUpClass(cls):
        if cls is BaseTestViewSet:
            raise unittest.SkipTest("Skip BaseTest tests, it's a base class")
        super(BaseTestViewSet, cls).setUpClass()

    def setUp(self):
        super(BaseTestViewSet, self).setUp()
        self.user = mixer.blend('auth.User')
        token = issue_token(self.user)
        self.client = APIClient()
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + token['token'])
        self.a_client = APIClient()

    def create_fixtures(self):
        raise NotImplemented

    def test_list(self):
        import pdb
        pdb.set_trace()
        resp = self.a_client.get(self.api_endpoint)
        assert resp.status_code == 401

        resp = self.client.get(self.api_endpoint)
        resp.render()
        data = json.loads(resp.content)
        assert resp.status_code == 200
        assert data['count'] == 0

        objs = self.create_fixtures()

        resp = self.client.get(self.api_endpoint)
        resp.render()
        data = json.loads(resp.content)
        assert resp.status_code == 200
        assert data['count'] == self.count


class ProjectTestCase(BaseTestViewSet):
    api_endpoint = '/api/projects/'

    def create_fixtures(self):
        return ProjectFactory.create_batch(self.count)
