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

from core.models import AccessToken, Profile, Tag
from project.factory import *
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


class BaseTestViewSet:
    api_endpoint = None
    count = 10
    factory = None

    def get_client(self, auth=False):
        if auth:
            return self.get_auth_client()
        return APIClient()

    def get_auth_client(self):
        user = mixer.blend('auth.User')
        self.user = user
        token = issue_token(user)
        self.token = token
        client = APIClient()
        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + token['token'])
        return client

    def create_fixtures(self):
        raise NotImplemented

    def testList(self):
        a_client = self.get_client(True)
        client = self.get_client()

        resp = client.get(self.api_endpoint)
        assert resp.status_code == 401

        resp = a_client.get(self.api_endpoint)
        resp.render()
        data = json.loads(resp.content)
        assert resp.status_code == 200
        assert data['count'] == 0

        objs = self.factory.create_batch(self.count)

        resp = a_client.get(self.api_endpoint)
        resp.render()
        data = json.loads(resp.content)
        assert resp.status_code == 200
        assert data['count'] == self.count

    def testRetrive(self):
        a_client = self.get_client(True)
        client = self.get_client()
        obj = self.factory.create()
        resp = client.get(self.api_endpoint + '%s/' % obj.pk)
        assert resp.status_code == 401

        resp = a_client.get(self.api_endpoint + '%s/' % obj.pk)
        resp.render()
        data = resp.json()
        assert resp.status_code == 200
        assert data['title'] == obj.title
        assert data['id'] == obj.id
        self.assertEqual(data['title'], obj.title, 'should equal')

    def testUpdate(self):
        pass


class ProjectTestCase(TestCase, BaseTestViewSet):

    api_endpoint = '/api/projects/'
    factory = ProjectFactory

    def create_fixtures(self):
        return ProjectFactory.create_batch(self.count)

    def test_create(self):
        client = self.get_client()
        a_client = self.get_client(True)

        payload = {'title': 'abc'}

        resp = client.post(self.api_endpoint, payload)
        self.assertEqual(resp.status_code, 401)

        resp = a_client.post(self.api_endpoint, payload, format='json')
        resp.render()
        data = json.loads(resp.content)
        assert resp.status_code == 201
        assert data['title'] == payload['title']
        assert data['owner']['id'] == self.user.id
        assert Project.objects.get(title=payload['title'])
        assert Project.objects.filter(title=payload['title']).count() == 1

        # same title will raise error
        resp = a_client.post(self.api_endpoint, payload, format='json')
        resp.render()
        assert resp.status_code == 400
        data = json.loads(resp.content)
        assert data['code'] == 400
        assert data['errors']['title']
        assert Project.objects.filter(title=payload['title']).count() == 1

        # with category


class UserTestCase(BaseTestViewSet):
    api_endpoint = '/api/users/'
    factory = UserFactory


class TagTestCase(BaseTestViewSet):
    api_endpoint = '/api/tags/'

    def create_fixtures(self):
        return TagFactory.create_batch(self.count)
