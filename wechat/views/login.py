import time
from django.conf import settings
from django.http import JsonResponse
from django.http.response import JsonResponse, HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.contrib.auth import authenticate, login

from api.serializers import UserSerializer
from wechatpy.oauth import WeChatOAuth
from rest_framework_jwt.settings import api_settings

from core.models import AccessToken, create_profile, SiteConf

User = get_user_model()

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


def issue_token(user):
    payload = jwt_payload_handler(user)
    return {
        'token': jwt_encode_handler(payload),
        'user': user
    }


def authorize(request):
    code = request.GET.get('code', '')
    # use state to track user id
    state = request.GET.get('state', '')
    config = SiteConf.get_solo()

    if not config.enable_wechat:
        return HttpResponseForbidden('没有开启微信登录')

    client = WeChatOAuth(config.wx_appid,
                         config.wx_appsecret,
                         config.wx_redirect_uri,
                         scope='snsapi_userinfo',
                         state=state)

    # auth flow
    if code:
        try:
            # may raise
            access_token = client.fetch_access_token(code)
            user_info = client.get_user_info()
            user, _ = User.objects.get_or_create(
                username='wx_' + access_token['openid'])

            # may raise IntegrityError 微信用户已经绑定了关系
            at, _ = AccessToken.objects.get_or_create(
                user=user, openid=access_token['openid'])
            at.update_token(access_token)

            # update profile
            user.profile.update_profile(user_info)
            token = issue_token(user)
            # login user
            login(request, user)

            # request.session.set_expiry(3600 * 24 * 7)  # 7days
            return redirect('wechat:index')
        except Exception as e:
            return HttpResponseForbidden('出错 {0}'.format(str(e)))

    return redirect(client.authorize_url)
