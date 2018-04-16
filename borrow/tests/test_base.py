import json
import pytest
from mixer.backend.django import mixer
from django.test import RequestFactory
from django.urls import reverse
from django.contrib.auth.models import Permission

pytestmark = pytest.mark.django_db


class BaseApiView:

    _view = None
    _view_url = ''
    _perm = None
    _test_api_chain = []

    def _test_no_perm(self, req):
        user = mixer.blend('auth.User')
        req.user = user
        resp = self._view.as_view()(req)
        assert resp.status_code == 200

        data = json.loads(resp.content)
        assert not data['status'] and data['code'] == -100, '应该返回没有权限的错误'

    def _get_data_with_perm(self, req, perm_name):
        user = mixer.blend('auth.User')

        req.user = user
        if self._perm is not None:
            req.user.user_permissions.add(
                Permission.objects.get(codename=getattr(self._perm, perm_name))
            )

        resp = self._view.as_view()(req)
        assert resp.status_code == 200

        data = json.loads(resp.content)
        assert data['code'] != -100, '应该通过权限检查'

        return data

    def test_api(self):
        for api_type, api_perm, has_pagination in self._test_api_chain:
            req = RequestFactory().post(reverse(self._view_url), {'type': api_type})
            self._test_no_perm(req)
            data = self._get_data_with_perm(req, api_perm)
            assert data['status'], data['msg']

            result = data['msg']
            if has_pagination:
                assert result.get('count', -1) >= 0, '获取分页数据失败'
