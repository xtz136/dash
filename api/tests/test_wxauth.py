from unittest.mock import patch
from django.urls import reverse
from django.test import TestCase
from django.conf import settings
from django.contrib.auth import get_user_model
from core.models import AccessToken, Profile


import pytest
from mixer.backend.django import mixer
pytestmark = pytest.mark.django_db

User = get_user_model()


fake_access_token = {"access_token": "ACCESS_TOKEN",
                     "expires_in": 7200,
                     "refresh_token": "REFRESH_TOKEN",
                     "openid": "OPENID",
                     "scope": "SCOPE"}

fake_user_info = {"openid": " OPENID",
                  "nickname": "nickname",
                  "sex": "1",
                  "province": "PROVINCE",
                  "city": "CITY",
                  "country": "COUNTRY",
                  "headimgurl": "http://wx.qlogo.cn/mmopen/g3MonUZtNHkdmzicIlibx6iaFqAc56vxLSUfpb6n5WKSYVY0ChQKkiaJSgQ1dZuTOgvLLrhJbERQQ",
                  "privilege": ["PRIVILEGE1" "PRIVILEGE2"],
                  "unionid": "o6_bmasdasdsad6_2sgVt7hMZOPfL"}


class WeChatTestCase(TestCase):
    def test_login_without_code(self):
        # without code should return 302
        resp = self.client.get(reverse('api:wechat_authorize'))
        assert resp.url.startswith(
            'https://open.weixin.qq.com/connect/oauth2/authorize?appid')
        assert resp.status_code == 302

    @patch('wechatpy.oauth.WeChatOAuth.fetch_access_token')
    @patch('wechatpy.oauth.WeChatOAuth.get_user_info')
    @patch('core.models.AccessToken.update_token')
    @patch('api.views.issue_token')
    @patch('core.models.Profile.update_profile')
    def test_login_with_code(self, update_profile, issue_token, update_token,  get_user_info, fetch_access_token):
        assert not AccessToken.objects.filter(
            openid=fake_access_token['openid']).exists()
        fetch_access_token.return_value = fake_access_token
        get_user_info.return_value = fake_user_info
        code = 'fakecode'
        resp = self.client.get(
            reverse('api:wechat_authorize') + "?code=" + code)

        update_profile.assert_called_once()
        update_token.assert_called_once()
        fetch_access_token.assert_called_with(code)
        get_user_info.assert_called_once()
        # issue_token.assert_called_once()

        self.assertEqual(resp.status_code, 200)
        qs = AccessToken.objects.filter(
            openid=fake_access_token['openid'])
        assert qs.count() == 1
        qs = User.objects.all()
        assert qs.count() == 1
