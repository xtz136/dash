import json
import pytest

from django.test import RequestFactory
from django.urls import reverse
from mixer.backend.django import mixer

from ..views import company

pytestmark = pytest.mark.django_db


class TestCompanyApiView(object):

    def test_api_list(self):
        req = RequestFactory().post(reverse('api.company'), {'type': 'api_list'})
        user = mixer.blend('auth.User')
        req.user = user
        resp = company.CompanyApiView.as_view()(req)
        assert resp.status_code == 200

        data = json.loads(resp.content)
        assert data['status'], data['msg']

        result = data['msg']
        assert result.get('count', -1) >= 0, '获取分页数据失败'
