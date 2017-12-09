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
from api.serializers import *
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

    def testAnonymousList(self):
        client = self.get_client(auth=False)
        resp = client.get(self.api_endpoint)
        assert resp.status_code == 401

    def testAnonymousCreate(self):
        client = self.get_client(auth=False)
        resp = client.post(self.api_endpoint, {}, format='json')
        assert resp.status_code == 401

    def testAnonymousRetrive(self):
        client = self.get_client(auth=False)
        obj = self.factory.create()
        resp = client.get(self.api_endpoint + '%d/' % obj.pk)
        assert resp.status_code == 401

    def testAnonymousUpdate(self):
        client = self.get_client(auth=False)
        obj = self.factory.create()
        resp = client.post(self.api_endpoint + '%d/' %
                           obj.pk, {}, format='json')
        assert resp.status_code == 401

    def testList(self):
        client = self.get_client(True)
        resp = client.get(self.api_endpoint)
        resp.render()
        data = json.loads(resp.content)
        assert resp.status_code == 200
        assert data['count'] == 0

        objs = self.factory.create_batch(self.count)
        resp = client.get(self.api_endpoint)
        resp.render()
        data = json.loads(resp.content)
        assert resp.status_code == 200
        assert data['count'] == self.count

    def testRetrive(self):
        client = self.get_client(True)
        obj = self.factory.create()
        resp = client.get(self.api_endpoint + '%s/' % obj.pk)
        resp.render()
        data = resp.json()
        assert resp.status_code == 200
        assert data['id'] == obj.id


class ProjectTestCase(TestCase, BaseTestViewSet):

    api_endpoint = '/api/projects/'
    factory = ProjectFactory

    def create_fixtures(self):
        return ProjectFactory.create_batch(self.count)

    def test_create(self):
        client = self.get_client(True)

        payload = {'title': 'abc'}

        resp = client.post(self.api_endpoint, {}, format='json')
        assert resp.status_code == 400, resp.content
        resp.render()

        resp = client.post(self.api_endpoint, payload, format='json')
        resp.render()
        data = json.loads(resp.content)
        assert resp.status_code == 201, data
        assert data['title'] == payload['title']
        assert data['owner']['id'] == self.user.id
        assert Project.objects.get(title=payload['title'])
        assert Project.objects.filter(title=payload['title']).count() == 1

        # same title will raise error
        resp = client.post(self.api_endpoint, payload, format='json')
        resp.render()
        assert resp.status_code == 400
        data = json.loads(resp.content)
        assert data['code'] == 400
        assert data['errors']['title']
        assert Project.objects.filter(title=payload['title']).count() == 1

        users = mixer.cycle(100).blend('auth.User')
        # with category
        tags = TagFactory.create_batch(10)
        cat = CategoryFactory.create()
        payload = {'title': 'jwqeofijq', 'category': cat.id,
                   'tags': [t.id for t in tags], 'members': [u.id for u in users]}
        resp = client.post(self.api_endpoint, payload, format='json')
        resp.render()
        data = json.loads(resp.content)
        assert resp.status_code == 201, data
        assert data['category']['id'] == cat.id, data
        assert data['category']['title'] == cat.title, data
        assert len(data['tags']) == len(tags)
        assert len(data['members']) == 100
        assert Project.objects.filter(title=payload['title']).count() == 1


class CategoryTestCase(TestCase, BaseTestViewSet):
    api_endpoint = '/api/categories/'
    factory = CategoryFactory


class TagTestCase(TestCase, BaseTestViewSet):
    api_endpoint = '/api/tags/'
    factory = TagFactory


class CompanyTestCase(TestCase, BaseTestViewSet):
    api_endpoint = '/api/company/'
    factory = CompanyFactory

    def test_fields_info(self):
        client = self.get_client(True)
        resp = client.get('/api/fields_info/?')
        resp.render()
        data = json.loads(resp.content)
        assert resp.status_code == 200, data

    def test_create(self):
        client = self.get_client(True)
        payload = {'title': 'aaa'}
        resp = client.post(self.api_endpoint, payload, format='json')
        resp.render()
        data = json.loads(resp.content)
        assert resp.status_code == 201, data
        assert data['title'] == payload['title']

        # same request

        payload = {'title': 'aaa'}
        resp = client.post(self.api_endpoint, payload, format='json')
        resp.render()
        data = json.loads(resp.content)
        assert resp.status_code == 400, data
