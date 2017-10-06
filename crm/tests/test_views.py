import pytest
from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser
from mixer.backend.django import mixer
from django.contrib.auth.models import User, Permission
from django.core.exceptions import PermissionDenied
pytestmark = pytest.mark.django_db

from .. import views
from .. import models


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


class TestClientDetailView:
    def test_anonymous(self):
        req = RequestFactory().get('/client/1/')
        client = mixer.blend('crm.company')
        req.user = AnonymousUser()
        resp = views.ClientDetailView.as_view()(req, pk=client.pk)
        assert resp.status_code == 302, '匿名不能访问'

    def test_superuser(self):
        req = RequestFactory().get('/client/1/')
        user = mixer.blend('auth.User', is_superuser=True)
        client = mixer.blend('crm.company')
        req.user = user
        resp = views.ClientDetailView.as_view()(req, pk=client.pk)
        assert resp.status_code == 200, '管理员能访问'


class TestLibraryView:
    def test_anonymous(self):
        req = RequestFactory().get('/customer/')
        req.user = AnonymousUser()
        resp = views.LibraryView.as_view()(req)
        assert resp.status_code == 302, '匿名不能访问'

    def test_superuser(self):
        req = RequestFactory().get('/dashboard/')
        user = mixer.blend('auth.User')
        req.user = user
        resp = views.LibraryView.as_view()(req)
        assert resp.status_code == 200, '普通用户能访问'


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


class TestClientCreateView:

    def test_create(self):
        data = {'title': '啊啊啊'}
        req = RequestFactory().post('/client/create/', data)
        req.user = AnonymousUser()
        with pytest.raises(PermissionDenied):
            resp = views.ClientCreateView.as_view()(req)

    def test_normal_user_create(self):
        data = {'title': '啊啊啊'}
        req = RequestFactory().post('/client/create/', data)
        req.user = mixer.blend('auth.User')
        with pytest.raises(PermissionDenied) as excinfo:
            resp = views.ClientCreateView.as_view()(req)
        assert '请联系管理员获取查看该页面的权限' in str(excinfo.value)

    def test_superuser_create(self):
        data = {'title': '我是公司抬头',
                'type': '有限责任公司',
                'industry': '汽配',
                'taxpayer_type': '小规模纳税人',
                'scale_size': '小型企业',
                'status': '有效',
                'credit_rating': '良好',
                'ic_status': '正常',
                'registered_capital': 1}
        req = RequestFactory().post('/client/create/', data)
        req.user = mixer.blend('auth.User', is_superuser=True)
        resp = views.ClientCreateView.as_view()(req)
        assert resp.status_code == 302
        c = models.Company.objects.get(title=data['title'])

        # detail
        req = RequestFactory().get('/client/{id}/'.format(id=c.id))
        req.user = mixer.blend('auth.User', is_superuser=True)
        resp = views.ClientDetailView.as_view()(req, pk=c.id)
        assert resp.status_code == 200
        assert data['title'] in resp.rendered_content

        # edit
        req = RequestFactory().get('/client/{id}/edit/'.format(id=c.id))
        req.user = mixer.blend('auth.User', is_superuser=True)
        resp = views.ClientEditView.as_view()(req, pk=c.id)
        assert resp.status_code == 200
        assert data['title'] in resp.rendered_content

    def test_authorize_user(self):
        user = mixer.blend('auth.User', is_active=True)
        perm = Permission.objects.get(codename='add_company')
        assert perm
        user.user_permissions.add(perm)
        assert user.has_perm('crm.add_company')

        data = {'title': '我是公司抬头',
                'type': '有限责任公司',
                'industry': '汽配',
                'taxpayer_type': '小规模纳税人',
                'scale_size': '小型企业',
                'status': '有效',
                'credit_rating': '良好',
                'ic_status': '正常',
                'registered_capital': 1}
        req = RequestFactory().post('/client/create/', data)
        req.user = user
        resp = views.ClientCreateView.as_view()(req)
        assert resp.status_code == 302
        c = models.Company.objects.get(title=data['title'])

        # detail
        req = RequestFactory().get('/client/{id}/'.format(id=c.id))
        req.user = user
        resp = views.ClientDetailView.as_view()(req, pk=c.id)
        assert resp.status_code == 200
        assert data['title'] in resp.rendered_content

        # edit
        req = RequestFactory().get('/client/{id}/edit/'.format(id=c.id))
        req.user = user
        with pytest.raises(PermissionDenied) as excinfo:
            resp = views.ClientEditView.as_view()(req, pk=c.id)
        assert '请联系管理员获取查看该页面的权限' in str(excinfo.value)

        # edit post
        data = {'title': '另一个抬头'}
        req = RequestFactory().post('/client/{id}/edit/'.format(id=c.id), data)
        req.user = user
        with pytest.raises(PermissionDenied) as excinfo:
            resp = views.ClientEditView.as_view()(req, pk=c.id)
        assert '请联系管理员获取查看该页面的权限' in str(excinfo.value)

        user = mixer.blend('auth.User', is_active=True)
        perm = Permission.objects.get(codename='change_company')
        assert perm, "修改公司应该存在"
        user.user_permissions.add(perm)
        # assert user.has_perm('crm.change_company'), "用户应该拥有修改公司的权限"

        # edit
        req = RequestFactory().get('/client/{id}/edit/'.format(id=c.id))
        req.user = user
        resp = views.ClientEditView.as_view()(req, pk=c.id)
        assert resp.status_code == 200

        # edit post
        data = {'title': '另一个抬头'}
        req = RequestFactory().post('/client/{id}/edit/'.format(id=c.id), data)
        req.user = user
        resp = views.ClientEditView.as_view()(req, pk=c.id)
        assert resp.status_code == 200
        assert data['title'] in resp.rendered_content
