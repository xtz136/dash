import pytest
from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser
from mixer.backend.django import mixer
from django.contrib.auth.models import User
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


class TestClientView:
    def test_anonymous(self):
        req = RequestFactory().get('/client/')
        req.user = AnonymousUser()
        resp = views.ClientView.as_view()(req)
        assert resp.status_code == 302, '匿名不能访问'

    def test_superuser(self):
        req = RequestFactory().get('/client/')
        user = mixer.blend('auth.User', is_superuser=True)
        req.user = user
        resp = views.ClientView.as_view()(req)
        assert resp.status_code == 200, '管理员能访问'


class TestLibraryView:
    def test_anonymous(self):
        req = RequestFactory().get('/customer/')
        req.user = AnonymousUser()
        resp = views.LibraryView.as_view()(req)
        assert resp.status_code == 302, '匿名不能访问'

    def test_superuser(self):
        req = RequestFactory().get('/dashboard/')
        user = mixer.blend('auth.User', is_superuser=True)
        req.user = user
        resp = views.LibraryView.as_view()(req)
        assert resp.status_code == 200, '管理员能访问'


class TestRegisterView:
    def test_register(self):
        req = RequestFactory().get('/accounts/register/')
        resp = views.UserCreateView.as_view()(req)
        assert resp.status_code == 200, '能正常访问注册页面'

    def test_create(self):
        data = {'username': 'u1', 'password1': 'abc', 'password2': 'abc'}
        req = RequestFactory().post('/accounts/register/', data)
        resp = views.UserCreateView.as_view()(req)
        assert '密码长度太短' in resp.rendered_content, '密码不能太短'

        assert User.objects.filter(username='u1').count() == 0, '不应该存在用户 u1'
        data = {'username': 'u1', 'password1': 'raise ContentNotRenderedError',
                'password2': 'raise ContentNotRenderedError'}
        req = RequestFactory().post('/accounts/register/', data)
        resp = views.UserCreateView.as_view()(req)
        u = User.objects.get(username='u1')
        assert u.check_password(data['password1']), '密码应该正确'

        assert not u.is_active, '创建的用户默认不激活'
