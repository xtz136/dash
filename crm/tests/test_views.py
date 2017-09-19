import pytest
from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser
from mixer.backend.django import mixer
pytestmark = pytest.mark.django_db

from .. import views


class TestDashboardView:
    def test_anonymous(self):
        req = RequestFactory().get('/dashboard/')
        req.user = AnonymousUser()
        resp = views.DashboardView.as_view()(req)
        assert resp.status_code == 302, '匿名不能访问'

    def test_superuser(self):
        req = RequestFactory().get('/dashboard/')
        user = mixer.blend('auth.User', is_superuser=True)
        req.user = user
        resp = views.DashboardView.as_view()(req)
        assert resp.status_code == 200, '管理员能访问'
